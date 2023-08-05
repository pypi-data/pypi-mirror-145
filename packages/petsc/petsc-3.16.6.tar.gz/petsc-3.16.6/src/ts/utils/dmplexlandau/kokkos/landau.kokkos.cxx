/*
  Implements the Kokkos kernel
*/
#include <petscconf.h>
#include <petscvec_kokkos.hpp>
#include <petsc/private/dmpleximpl.h>   /*I   "petscdmplex.h"   I*/
#include <petsclandau.h>
#include <petscts.h>

#include <Kokkos_Core.hpp>
#include <cstdio>
typedef Kokkos::TeamPolicy<>::member_type team_member;
#include "../land_tensors.h"
#include <petscaijdevice.h>

namespace landau_inner_red {  // namespace helps with name resolution in reduction identity
  template< class ScalarType >
  struct array_type {
    ScalarType gg2[LANDAU_DIM];
    ScalarType gg3[LANDAU_DIM][LANDAU_DIM];

    KOKKOS_INLINE_FUNCTION   // Default constructor - Initialize to 0's
    array_type() {
      for (int j = 0; j < LANDAU_DIM; j++) {
        gg2[j] = 0;
        for (int k = 0; k < LANDAU_DIM; k++) {
          gg3[j][k] = 0;
        }
      }
    }
    KOKKOS_INLINE_FUNCTION   // Copy Constructor
    array_type(const array_type & rhs) {
      for (int j = 0; j < LANDAU_DIM; j++) {
        gg2[j] = rhs.gg2[j];
        for (int k = 0; k < LANDAU_DIM; k++) {
          gg3[j][k] = rhs.gg3[j][k];
        }
      }
    }
    KOKKOS_INLINE_FUNCTION   // add operator
    array_type& operator += (const array_type& src)
    {
      for (int j = 0; j < LANDAU_DIM; j++) {
        gg2[j] += src.gg2[j];
        for (int k = 0; k < LANDAU_DIM; k++) {
          gg3[j][k] += src.gg3[j][k];
        }
      }
      return *this;
    }
    KOKKOS_INLINE_FUNCTION   // volatile add operator
    void operator += (const volatile array_type& src) volatile
    {
      for (int j = 0; j < LANDAU_DIM; j++) {
        gg2[j] += src.gg2[j];
        for (int k = 0; k < LANDAU_DIM; k++) {
          gg3[j][k] += src.gg3[j][k];
        }
      }
    }
  };
  typedef array_type<PetscReal> TensorValueType;  // used to simplify code below
}

namespace Kokkos { //reduction identity must be defined in Kokkos namespace
  template<>
  struct reduction_identity< landau_inner_red::TensorValueType > {
    KOKKOS_FORCEINLINE_FUNCTION static landau_inner_red::TensorValueType sum() {
      return landau_inner_red::TensorValueType();
    }
  };
}

extern "C"  {
PetscErrorCode LandauKokkosCreateMatMaps(P4estVertexMaps maps[], pointInterpolationP4est (*pointMaps)[LANDAU_MAX_Q_FACE], PetscInt Nf[], PetscInt Nq, PetscInt grid)
{
  P4estVertexMaps   h_maps;  /* host container */
  const Kokkos::View<pointInterpolationP4est*[LANDAU_MAX_Q_FACE], Kokkos::LayoutRight, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> >    h_points ((pointInterpolationP4est*)pointMaps, maps[grid].num_reduced);
  const Kokkos::View< LandauIdx*[LANDAU_MAX_SPECIES][LANDAU_MAX_NQ], Kokkos::LayoutRight, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_gidx ((LandauIdx*)maps[grid].gIdx, maps[grid].num_elements);
  Kokkos::View<pointInterpolationP4est*[LANDAU_MAX_Q_FACE], Kokkos::LayoutRight>   *d_points = new Kokkos::View<pointInterpolationP4est*[LANDAU_MAX_Q_FACE], Kokkos::LayoutRight>("points", maps[grid].num_reduced);
  Kokkos::View<LandauIdx*[LANDAU_MAX_SPECIES][LANDAU_MAX_NQ], Kokkos::LayoutRight> *d_gidx = new Kokkos::View<LandauIdx*[LANDAU_MAX_SPECIES][LANDAU_MAX_NQ], Kokkos::LayoutRight>("gIdx", maps[grid].num_elements);

  PetscFunctionBegin;
  Kokkos::deep_copy (*d_gidx, h_gidx);
  Kokkos::deep_copy (*d_points, h_points);
  h_maps.num_elements = maps[grid].num_elements;
  h_maps.num_face = maps[grid].num_face;
  h_maps.num_reduced = maps[grid].num_reduced;
  h_maps.deviceType = maps[grid].deviceType;
  h_maps.numgrids = maps[grid].numgrids;
  h_maps.Nf = Nf[grid];
  h_maps.Nq = Nq;
  h_maps.c_maps = (pointInterpolationP4est (*)[LANDAU_MAX_Q_FACE]) d_points->data();
  maps[grid].vp1 = (void*)d_points;
  h_maps.gIdx = (LandauIdx (*)[LANDAU_MAX_SPECIES][LANDAU_MAX_NQ]) d_gidx->data();
  maps[grid].vp2 = (void*)d_gidx;
  {
    Kokkos::View<P4estVertexMaps, Kokkos::HostSpace> h_maps_k(&h_maps);
    Kokkos::View<P4estVertexMaps>                    *d_maps_k = new Kokkos::View<P4estVertexMaps>(Kokkos::create_mirror(Kokkos::DefaultExecutionSpace::memory_space(),h_maps_k));
    Kokkos::deep_copy (*d_maps_k, h_maps_k);
    maps[grid].d_self = d_maps_k->data();
    maps[grid].vp3 = (void*)d_maps_k;
  }
  PetscFunctionReturn(0);
}
PetscErrorCode LandauKokkosDestroyMatMaps(P4estVertexMaps maps[], PetscInt num_grids)
{
  PetscFunctionBegin;
  for (PetscInt grid=0;grid<num_grids;grid++) {
    auto a = static_cast<Kokkos::View<pointInterpolationP4est*[LANDAU_MAX_Q_FACE], Kokkos::LayoutRight>*>(maps[grid].vp1);
    auto b = static_cast<Kokkos::View<LandauIdx*[LANDAU_MAX_SPECIES][LANDAU_MAX_NQ], Kokkos::LayoutRight>*>(maps[grid].vp2);
    auto c = static_cast<Kokkos::View<P4estVertexMaps*>*>(maps[grid].vp3);
    delete a;  delete b;  delete c;
  }
  PetscFunctionReturn(0);
}

PetscErrorCode LandauKokkosStaticDataSet(DM plex, const PetscInt Nq, const PetscInt num_grids, PetscInt a_numCells[], PetscInt a_species_offset[], PetscInt a_mat_offset[],
                                         PetscReal a_nu_alpha[], PetscReal a_nu_beta[], PetscReal a_invMass[], PetscReal a_invJ[],
                                         PetscReal a_x[], PetscReal a_y[], PetscReal a_z[], PetscReal a_w[], LandauStaticData *SData_d)
{
  PetscReal       *BB,*DD;
  PetscErrorCode  ierr;
  PetscTabulation *Tf;
  PetscInt        dim;
  PetscInt        Nb=Nq,ip_offset[LANDAU_MAX_GRIDS+1],ipf_offset[LANDAU_MAX_GRIDS+1],elem_offset[LANDAU_MAX_GRIDS+1],nip,IPf_sz,Nftot;
  PetscDS         prob;

  PetscFunctionBegin;
  ierr = DMGetDimension(plex, &dim);CHKERRQ(ierr);
  ierr = DMGetDS(plex, &prob);CHKERRQ(ierr);
  if (LANDAU_DIM != dim) SETERRQ2(PETSC_COMM_WORLD, PETSC_ERR_PLIB, "dim %D != LANDAU_DIM %d",dim,LANDAU_DIM);
  ierr = PetscDSGetTabulation(prob, &Tf);CHKERRQ(ierr);
  BB   = Tf[0]->T[0]; DD = Tf[0]->T[1];
  ip_offset[0] = ipf_offset[0] = elem_offset[0] = 0;
  nip = 0;
  IPf_sz = 0;
  for (PetscInt grid=0 ; grid<num_grids ; grid++) {
    PetscInt nfloc = a_species_offset[grid+1] - a_species_offset[grid];
    elem_offset[grid+1] = elem_offset[grid] + a_numCells[grid];
    nip += a_numCells[grid]*Nq;
    ip_offset[grid+1] = nip;
    IPf_sz += Nq*nfloc*a_numCells[grid];
    ipf_offset[grid+1] = IPf_sz;
  }
  Nftot = a_species_offset[num_grids];
  ierr = PetscKokkosInitializeCheck();CHKERRQ(ierr);
  {
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_alpha (a_nu_alpha, Nftot);
    auto alpha = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("alpha", Nftot);
    SData_d->alpha = static_cast<void*>(alpha);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_beta (a_nu_beta, Nftot);
    auto beta = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("beta", Nftot);
    SData_d->beta = static_cast<void*>(beta);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_invMass (a_invMass,Nftot);
    auto invMass = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("invMass", Nftot);
    SData_d->invMass = static_cast<void*>(invMass);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_BB (BB,Nq*Nb);
    auto B = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("B", Nq*Nb);
    SData_d->B = static_cast<void*>(B);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_DD (DD,Nq*Nb*dim);
    auto D = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("D", Nq*Nb*dim);
    SData_d->D = static_cast<void*>(D);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_invJ (a_invJ, nip*dim*dim);
    auto invJ = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("invJ", nip*dim*dim);
    SData_d->invJ = static_cast<void*>(invJ);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_x (a_x, nip);
    auto x = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("x", nip);
    SData_d->x = static_cast<void*>(x);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_y (a_y, nip);
    auto y = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("y", nip);
    SData_d->y = static_cast<void*>(y);
    const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_w (a_w, nip);
    auto w = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("w", nip);
    SData_d->w = static_cast<void*>(w);

    Kokkos::deep_copy (*alpha, h_alpha);
    Kokkos::deep_copy (*beta, h_beta);
    Kokkos::deep_copy (*invMass, h_invMass);
    Kokkos::deep_copy (*B, h_BB);
    Kokkos::deep_copy (*D, h_DD);
    Kokkos::deep_copy (*invJ, h_invJ);
    Kokkos::deep_copy (*x, h_x);
    Kokkos::deep_copy (*y, h_y);
    Kokkos::deep_copy (*w, h_w);

    if (dim==3) {
      const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_z (a_z , dim==3 ? nip : 0);
      auto z = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("z", nip);
      SData_d->z = static_cast<void*>(z);
      Kokkos::deep_copy (*z, h_z);
    } else SData_d->z = NULL;

    //
    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_NCells (a_numCells, num_grids);
    auto nc = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("NCells",num_grids);
    SData_d->NCells = static_cast<void*>(nc);
    Kokkos::deep_copy (*nc, h_NCells);

    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_species_offset (a_species_offset, num_grids+1);
    auto soff = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("species_offset",num_grids+1);
    SData_d->species_offset = static_cast<void*>(soff);
    Kokkos::deep_copy (*soff, h_species_offset);

    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_mat_offset (a_mat_offset, num_grids+1);
    auto moff = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("mat_offset",num_grids+1);
    SData_d->mat_offset = static_cast<void*>(moff);
    Kokkos::deep_copy (*moff, h_mat_offset);

    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_ip_offset (ip_offset, num_grids+1);
    auto ipoff = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("ip_offset",num_grids+1);
    SData_d->ip_offset = static_cast<void*>(ipoff);
    Kokkos::deep_copy (*ipoff,  h_ip_offset);

    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_elem_offset (elem_offset, num_grids+1);
    auto eoff = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("elem_offset",num_grids+1);
    SData_d->elem_offset = static_cast<void*>(eoff);
    Kokkos::deep_copy (*eoff,  h_elem_offset);

    const Kokkos::View<PetscInt*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_ipf_offset (ipf_offset, num_grids+1);
    auto ipfoff = new Kokkos::View<PetscInt*, Kokkos::LayoutLeft> ("ipf_offset",num_grids+1);
    SData_d->ipf_offset = static_cast<void*>(ipfoff);
    Kokkos::deep_copy (*ipfoff,  h_ipf_offset);

#if defined(LANDAU_LAYOUT_LEFT) // preallocate dynamic data, no copy
    auto ipfdf_data =  new Kokkos::View<PetscReal**, Kokkos::LayoutLeft > ("fdf", dim+1, IPf_sz);
#else
    auto ipfdf_data =  new Kokkos::View<PetscReal**, Kokkos::LayoutRight > ("fdf", dim+1, IPf_sz);
#endif
    SData_d->ipfdf_data = static_cast<void*>(ipfdf_data);

    auto Eq_m = new Kokkos::View<PetscReal*, Kokkos::LayoutLeft> ("Eq_m",Nftot); // allocate but do not set
    SData_d->Eq_m = static_cast<void*>(Eq_m);
  }
  SData_d->maps = NULL; // not used
  PetscFunctionReturn(0);
}

PetscErrorCode LandauKokkosStaticDataClear(LandauStaticData *SData_d)
{
  PetscFunctionBegin;
  if (SData_d->alpha) {
    auto alpha = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->alpha);
    delete alpha;
    SData_d->alpha = NULL;
    auto beta = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->beta);
    delete beta;
    auto invMass = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->invMass);
    delete invMass;
    auto B = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->B);
    delete B;
    auto D = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->D);
    delete D;
    auto invJ = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->invJ);
    delete invJ;
    auto x = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->x);
    delete x;
    auto y = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->y);
    delete y;
    if (SData_d->z) {
      auto z = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->z);
      delete z;
    }
#if defined(LANDAU_LAYOUT_LEFT) // preallocate dynamic data, no copy
    auto z = static_cast<Kokkos::View<PetscReal**, Kokkos::LayoutLeft>*>(SData_d->ipfdf_data);
#else
    auto z = static_cast<Kokkos::View<PetscReal**, Kokkos::LayoutRight>*>(SData_d->ipfdf_data);
#endif
    delete z;
    auto w = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->w);
    delete w;
    auto Eq_m = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->Eq_m);
    delete Eq_m;
    // offset
    auto nc = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->NCells);
    delete nc;
    auto soff = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->species_offset);
    delete soff;
    auto moff = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->mat_offset);
    delete moff;
    auto ipoff = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->ip_offset);
    delete ipoff;
    auto eoff = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->elem_offset);
    delete eoff;
    auto ipfoff = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->ipf_offset);
    delete ipfoff;
  }
  PetscFunctionReturn(0);
}

#define KOKKOS_SHARED_LEVEL 1
KOKKOS_INLINE_FUNCTION
PetscErrorCode landau_mat_assemble(PetscSplitCSRDataStructure d_mat, const team_member team,
                                   Kokkos::View<PetscScalar**, Kokkos::LayoutRight, Kokkos::DefaultExecutionSpace::scratch_memory_space> s_fieldMats,
                                   Kokkos::View<PetscInt**, Kokkos::LayoutRight, Kokkos::DefaultExecutionSpace::scratch_memory_space>  s_idx,
                                   Kokkos::View<PetscReal**, Kokkos::LayoutRight, Kokkos::DefaultExecutionSpace::scratch_memory_space> s_scale,
                                   const PetscInt Nb, const PetscInt Nq, const PetscInt nfaces, const PetscInt moffset, const PetscInt elem, const PetscInt fieldA, const P4estVertexMaps *d_maps)
{
  const LandauIdx *const Idxs = &d_maps->gIdx[elem][fieldA][0];
  team.team_barrier();
  Kokkos::parallel_for(Kokkos::TeamVectorRange(team,0,Nb), [=] (int f) {
      PetscInt q, idx = Idxs[f];
      if (idx >= 0) {
        s_idx(f,0) = idx + moffset;
        s_scale(f,0) = 1.;
      } else {
        idx = -idx - 1;
        for (q = 0; q < nfaces; q++) {
          s_idx(f,q) = d_maps->c_maps[idx][q].gid + moffset;
          s_scale(f,q) = d_maps->c_maps[idx][q].scale;
        }
      }
    });
  team.team_barrier();
  Kokkos::parallel_for(Kokkos::TeamThreadRange(team,0,Nb), [=] (int f) {
      PetscInt nr,idx = Idxs[f];
      if (idx >= 0) {
        nr = 1;
      } else {
        nr = nfaces;
      }
      Kokkos::parallel_for(Kokkos::ThreadVectorRange(team,0,Nb), [=] (int g) {
          PetscScalar     vals[LANDAU_MAX_Q_FACE*LANDAU_MAX_Q_FACE];
          PetscInt        q,d,nc,idx = Idxs[g];
          if (idx >= 0) {
            nc = 1;
          } else {
            nc = nfaces;
          }
          for (q = 0; q < nr; q++) {
            for (d = 0; d < nc; d++) {
              vals[q*nc + d] = s_scale(f,q)*s_scale(g,d)*s_fieldMats(f,g);
            }
          }
          MatSetValuesDevice(d_mat,nr,&s_idx(f,0),nc,&s_idx(g,0),vals,ADD_VALUES);
        });
    });
  return 0;
}

PetscErrorCode LandauKokkosJacobian(DM plex[], const PetscInt Nq, const PetscInt num_grids, const PetscInt a_numCells[], PetscReal a_Eq_m[], PetscScalar a_elem_closure[],
                                    const PetscInt N, const PetscScalar a_xarray[], const LandauStaticData *SData_d, const PetscInt num_sub_blocks, const PetscReal shift,
                                    const PetscLogEvent events[], const PetscInt a_mat_offset[], const PetscInt a_species_offset[], Mat subJ[], Mat JacP)
{
  using scr_mem_t = Kokkos::DefaultExecutionSpace::scratch_memory_space;
  using fieldMats_scr_t = Kokkos::View<PetscScalar**, Kokkos::LayoutRight, scr_mem_t>;
  using idx_scr_t = Kokkos::View<PetscInt**, Kokkos::LayoutRight, scr_mem_t>;
  using scale_scr_t = Kokkos::View<PetscReal**, Kokkos::LayoutRight, scr_mem_t>;
  using g2_scr_t = Kokkos::View<PetscReal***, Kokkos::LayoutRight, scr_mem_t>;
  using g3_scr_t = Kokkos::View<PetscReal****, Kokkos::LayoutRight, scr_mem_t>;
  PetscErrorCode    ierr;
  PetscInt          Nb=Nq,dim,num_cells_max,num_cells_tot,Nf_max,nip_global;
  int               nfaces=0;
  LandauCtx         *ctx;
  PetscReal         *d_Eq_m=NULL;
  PetscScalar       *d_vertex_f=NULL;
  P4estVertexMaps   *maps[LANDAU_MAX_GRIDS]; // this gets captured
  PetscSplitCSRDataStructure d_mat;
  PetscContainer    container = NULL;
  const int         conc = Kokkos::DefaultExecutionSpace().concurrency(), openmp = !!(conc < 1000), team_size = (openmp==0) ? Nq : 1;
  auto              d_alpha_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->alpha); //static data
  const PetscReal   *d_alpha = d_alpha_k->data();
  const PetscInt    Nftot = d_alpha_k->size(); // total number of species
  auto              d_beta_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->beta);
  const PetscReal   *d_beta = d_beta_k->data();
  auto              d_invMass_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->invMass);
  const PetscReal   *d_invMass = d_invMass_k->data();
  auto              d_B_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->B);
  const PetscReal   *d_BB = d_B_k->data();
  auto              d_D_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->D);
  const PetscReal   *d_DD = d_D_k->data();
  auto              d_invJ_k = *static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->invJ);     // use Kokkos vector in kernels
  auto              d_x_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->x); //static data
  const PetscReal   *d_x = d_x_k->data();
  auto              d_y_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->y); //static data
  const PetscReal   *d_y = d_y_k->data();
  auto              d_z_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->z); //static data
  const PetscReal   *d_z = (LANDAU_DIM==3) ? d_z_k->data() : NULL;
  auto              d_w_k = *static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->w); //static data
  const PetscReal   *d_w = d_w_k.data();
  auto              d_Eq_m_k = static_cast<Kokkos::View<PetscReal*, Kokkos::LayoutLeft>*>(SData_d->Eq_m); // static storage, dynamci data - E(t), copy later
  // grid offset d_numCells
  auto              d_numCells_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->NCells);
  const PetscInt   *d_numCells = d_numCells_k->data();
  auto              d_species_offset_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->species_offset);
  const PetscInt   *d_species_offset = d_species_offset_k->data();
  auto              d_mat_offset_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->mat_offset);
  const PetscInt   *d_mat_offset = d_mat_offset_k->data();
  auto              d_ip_offset_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->ip_offset);
  const PetscInt   *d_ip_offset = d_ip_offset_k->data();
  auto              d_ipf_offset_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->ipf_offset);
  const PetscInt   *d_ipf_offset = d_ipf_offset_k->data();
  auto              d_elem_offset_k = static_cast<Kokkos::View<PetscInt*, Kokkos::LayoutLeft>*>(SData_d->elem_offset);
  const PetscInt   *d_elem_offset = d_elem_offset_k->data();
#if defined(LANDAU_LAYOUT_LEFT) // preallocate dynamic data, no copy
  Kokkos::View<PetscReal**, Kokkos::LayoutLeft > d_fdf_k = *static_cast<Kokkos::View<PetscReal**, Kokkos::LayoutLeft >*>(SData_d->ipfdf_data);
#else
  Kokkos::View<PetscReal**, Kokkos::LayoutRight > d_fdf_k = *static_cast<Kokkos::View<PetscReal**, Kokkos::LayoutRight >*>(SData_d->ipfdf_data);
#endif
  PetscFunctionBegin;
  ierr = PetscLogEventBegin(events[3],0,0,0,0);CHKERRQ(ierr);
  ierr = DMGetApplicationContext(plex[0], &ctx);CHKERRQ(ierr);
  if (!ctx) SETERRQ(PETSC_COMM_SELF, PETSC_ERR_PLIB, "no context");
  ierr = DMGetDimension(plex[0], &dim);CHKERRQ(ierr);
  if (LANDAU_DIM != dim) SETERRQ2(PETSC_COMM_WORLD, PETSC_ERR_PLIB, "dim %D != LANDAU_DIM %d",dim,LANDAU_DIM);
  if (ctx->gpu_assembly) {
    ierr = PetscObjectQuery((PetscObject) JacP, "assembly_maps", (PetscObject *) &container);CHKERRQ(ierr);
    if (container) { // not here first call
      P4estVertexMaps   *h_maps=NULL;
      ierr = PetscContainerGetPointer(container, (void **) &h_maps);CHKERRQ(ierr);
      for (PetscInt grid=0 ; grid<num_grids ; grid++) {
        if (h_maps[grid].d_self) {
          maps[grid] = h_maps[grid].d_self;
          nfaces = h_maps[grid].num_face; // nface=0 for CPU assembly
        } else {
          SETERRQ(PETSC_COMM_SELF, PETSC_ERR_PLIB, "GPU assembly but no metadata in container");
        }
      }
      // this does the setup the first time called
      ierr = MatKokkosGetDeviceMatWrite(JacP,&d_mat);CHKERRQ(ierr);
    } else { // kernel output - first call assembled on device
      for (PetscInt grid=0 ; grid<num_grids ; grid++) maps[grid] = NULL;
      nfaces = 0;
    }
  } else {
    for (PetscInt grid=0 ; grid<num_grids ; grid++) maps[grid] = NULL;
    nfaces = 0;
  }
  nip_global = num_cells_tot = Nf_max = num_cells_max = 0;
  for (PetscInt grid=0 ; grid<num_grids ; grid++) {
    int Nfloc = a_species_offset[grid+1] - a_species_offset[grid];
    if (Nfloc > Nf_max) Nf_max = Nfloc;
    if (a_numCells[grid] > num_cells_max) num_cells_max = a_numCells[grid];
    num_cells_tot += a_numCells[grid];
    nip_global += Nq*a_numCells[grid];
  }
  const PetscInt totDim_max = Nf_max*Nq, elem_mat_size_max = totDim_max*totDim_max;
  const PetscInt elem_mat_num_cells_max_grid = container ? 0 : num_cells_max;
  Kokkos::View<PetscScalar***, Kokkos::LayoutRight> d_elem_mats("element matrices", num_grids, elem_mat_num_cells_max_grid, elem_mat_size_max); // first call have large set of global element matrices
  const Kokkos::View<PetscReal*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> >  h_Eq_m_k (a_Eq_m, Nftot);
  if (a_elem_closure || a_xarray) {
    Kokkos::deep_copy (*d_Eq_m_k, h_Eq_m_k);
    d_Eq_m = d_Eq_m_k->data();
  } else d_Eq_m = NULL;
  ierr = PetscKokkosInitializeCheck();CHKERRQ(ierr);
  ierr = PetscLogEventEnd(events[3],0,0,0,0);CHKERRQ(ierr);
  if (a_elem_closure || a_xarray) { // Jacobian, create f & df
    Kokkos::View<PetscScalar*, Kokkos::LayoutLeft> *d_vertex_f_k = NULL;
    ierr = PetscLogEventBegin(events[1],0,0,0,0);CHKERRQ(ierr);
    if (a_elem_closure) {
      PetscInt closure_sz = 0; // argh, don't have this on the host!!!
      for (PetscInt grid=0 ; grid<num_grids ; grid++) {
        PetscInt nfloc = a_species_offset[grid+1] - a_species_offset[grid];
        closure_sz     += Nq*nfloc*a_numCells[grid];
      }
      d_vertex_f_k = new Kokkos::View<PetscScalar*, Kokkos::LayoutLeft> ("closure",closure_sz);
      const Kokkos::View<PetscScalar*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryTraits<Kokkos::Unmanaged> > h_closure_k (a_elem_closure, closure_sz); // Vertex data for each element
      Kokkos::deep_copy (*d_vertex_f_k, h_closure_k);
      d_vertex_f  = d_vertex_f_k->data();
    } else {
      d_vertex_f = (PetscScalar*)a_xarray;
    }
    ierr = PetscLogEventEnd(events[1],0,0,0,0);CHKERRQ(ierr);
    ierr = PetscLogEventBegin(events[8],0,0,0,0);CHKERRQ(ierr);
    ierr = PetscLogGpuTimeBegin();CHKERRQ(ierr);
    Kokkos::parallel_for("f, df", Kokkos::TeamPolicy<>(num_cells_tot, team_size, /* Kokkos::AUTO */ 16), KOKKOS_LAMBDA (const team_member team) {
        // find my grid
        PetscInt grid = 0, g_cell = team.league_rank();
        while (g_cell >= d_elem_offset[grid+1]) grid++; // yuck search for grid
        {
          const PetscInt     moffset = d_mat_offset[grid], nip_loc = d_numCells[grid]*Nq, Nfloc = d_species_offset[grid+1] - d_species_offset[grid], elem = g_cell -  d_elem_offset[grid];
          const PetscInt     IP_idx = d_ip_offset[grid], IPf_idx = d_ipf_offset[grid];
          const PetscScalar  *coef;
          PetscScalar        coef_buff[LANDAU_MAX_SPECIES*LANDAU_MAX_NQ];
          // un pack IPData
          if (!maps[grid]) {
            coef = &d_vertex_f[elem*Nb*Nfloc + IPf_idx]; // closure and IP indexing are the same
          } else {
            coef = coef_buff;
            for (int f = 0; f < Nfloc; ++f) {
              LandauIdx *const Idxs = &maps[grid]->gIdx[elem][f][0];
              for (int b = 0; b < Nb; ++b) {
                PetscInt idx = Idxs[b];
                if (idx >= 0) {
                  coef_buff[f*Nb+b] = d_vertex_f[idx+moffset]; // xarray data, not IP
                } else {
                  idx = -idx - 1;
                  coef_buff[f*Nb+b] = 0;
                  for (int q = 0; q < maps[grid]->num_face; q++) {
                    PetscInt    id = maps[grid]->c_maps[idx][q].gid;
                    PetscScalar scale = maps[grid]->c_maps[idx][q].scale;
                    coef_buff[f*Nb+b] += scale*d_vertex_f[id+moffset];
                  }
                }
              }
            }
          }
          Kokkos::parallel_for(Kokkos::TeamThreadRange(team,0,Nq), [=] (int myQi) {
              const PetscInt          ipidx = IP_idx + myQi + elem * Nq, ipidx_g = myQi + elem * Nq;
              const PetscReal *const  invJj = &d_invJ_k(ipidx*dim*dim);
              const PetscReal         *Bq = &d_BB[myQi*Nb], *Dq = &d_DD[myQi*Nb*dim];
              Kokkos::parallel_for(Kokkos::ThreadVectorRange(team,0,(int)Nfloc), [=] (int f) {
                  PetscInt   b, e, d;
                  PetscReal  refSpaceDer[LANDAU_DIM];
                  const PetscInt idx = IPf_idx + f*nip_loc + ipidx_g;
                  d_fdf_k(0,idx) = 0.0;
                  for (d = 0; d < LANDAU_DIM; ++d) refSpaceDer[d] = 0.0;
                  for (b = 0; b < Nb; ++b) {
                    const PetscInt    cidx = b;
                    d_fdf_k(0,idx) += Bq[cidx]*PetscRealPart(coef[f*Nb+cidx]);
                    for (d = 0; d < dim; ++d) refSpaceDer[d] += Dq[cidx*dim+d]*PetscRealPart(coef[f*Nb+cidx]);
                  }
                  for (d = 0; d < dim; ++d) {
                    for (e = 0, d_fdf_k(d+1,idx) = 0.0; e < dim; ++e) {
                      d_fdf_k(d+1,idx) += invJj[e*dim+d]*refSpaceDer[e];
                    }
                  }
                }); // f
            }); // myQi
        }
      }); // global elems - fdf
    // #if defined(PETSC_HAVE_CUDA) || defined(PETSC_HAVE_HIP)
    //     ierr = PetscLogGpuFlops(nip_loc*(PetscLogDouble)(2*Nb*(1+dim)));CHKERRQ(ierr);
    // #else
    //     ierr = PetscLogFlops(nip_loc*(PetscLogDouble)(2*Nb*(1+dim)));CHKERRQ(ierr);
    // #endif
    Kokkos::fence();
    ierr = PetscLogGpuTimeEnd();CHKERRQ(ierr); // is this a fence?
    ierr = PetscLogEventEnd(events[8],0,0,0,0);CHKERRQ(ierr);
    if (d_vertex_f_k) delete d_vertex_f_k;
    // Jacobian
    ierr = PetscLogEventBegin(events[4],0,0,0,0);CHKERRQ(ierr);
    ierr = PetscLogGpuTimeBegin();CHKERRQ(ierr);
    // #if defined(PETSC_HAVE_CUDA) || defined(PETSC_HAVE_HIP)
    //           ierr = PetscLogGpuFlops(nip_loc*(PetscLogDouble)((nip_loc*(11*Nfloc+ 4*dim*dim) + 6*Nfloc*dim*dim*dim + 10*Nfloc*dim*dim + 4*Nfloc*dim + Nb*Nfloc*Nb*Nq*dim*dim*5)));CHKERRQ(ierr);
    // #else
    //           ierr = PetscLogFlops(nip_loc*(PetscLogDouble)((nip_loc*(11*Nfloc+ 4*dim*dim) + 6*Nfloc*dim*dim*dim + 10*Nfloc*dim*dim + 4*Nfloc*dim + Nb*Nfloc*Nb*Nq*dim*dim*5)));CHKERRQ(ierr);
    // #endif
    const int scr_bytes = 2*(g2_scr_t::shmem_size(dim,Nf_max,Nq) + g3_scr_t::shmem_size(dim,dim,Nf_max,Nq))+fieldMats_scr_t::shmem_size(Nb,Nb)+idx_scr_t::shmem_size(Nb,nfaces)+scale_scr_t::shmem_size(Nb,nfaces);
    ierr = PetscInfo6(plex[0], "Jacobian shared memory size: %d bytes in level %d num_cells_tot=%D team size=%D #face=%D Nf_max=%D\n",scr_bytes,KOKKOS_SHARED_LEVEL,num_cells_tot,team_size,nfaces,Nf_max);CHKERRQ(ierr);
    Kokkos::parallel_for("Jacobian", Kokkos::TeamPolicy<>(num_cells_tot, team_size, /* Kokkos::AUTO */ 16).set_scratch_size(KOKKOS_SHARED_LEVEL, Kokkos::PerTeam(scr_bytes)), KOKKOS_LAMBDA (const team_member team) {
        // find my grid
        PetscInt grid = 0, g_cell = team.league_rank();
        while (g_cell >= d_elem_offset[grid+1]) grid++; // yuck search for grid
        {
          const PetscInt  moffset = d_mat_offset[grid], Nfloc = d_species_offset[grid+1]-d_species_offset[grid], elem = g_cell-d_elem_offset[grid], totDim = Nfloc*Nq;
          const PetscInt  IP_idx = d_ip_offset[grid];
          const PetscInt  f_off = d_species_offset[grid];
          g2_scr_t        g2(team.team_scratch(KOKKOS_SHARED_LEVEL),dim,Nfloc,Nq);
          g3_scr_t        g3(team.team_scratch(KOKKOS_SHARED_LEVEL),dim,dim,Nfloc,Nq);
          g2_scr_t        gg2(team.team_scratch(KOKKOS_SHARED_LEVEL),dim,Nfloc,Nq);
          g3_scr_t        gg3(team.team_scratch(KOKKOS_SHARED_LEVEL),dim,dim,Nfloc,Nq);
          // get g2[] & g3[]
          Kokkos::parallel_for(Kokkos::TeamThreadRange(team,0,Nq), [=] (int myQi) {
              using Kokkos::parallel_reduce;
              const PetscInt                    jpidx_g = myQi + elem * Nq, jpidx = IP_idx + jpidx_g;
              const PetscReal* const            invJj = &d_invJ_k(jpidx*dim*dim);
              const PetscReal                   vj[3] = {d_x[jpidx], d_y[jpidx], d_z ? d_z[jpidx] : 0}, wj = d_w[jpidx];
              landau_inner_red::TensorValueType gg_temp; // reduce on part of gg2 and g33 for IP jpidx_g
              Kokkos::parallel_reduce(Kokkos::ThreadVectorRange (team, (int)nip_global), [=] (const int& ipidx, landau_inner_red::TensorValueType & ggg) {
                  const PetscReal wi = d_w[ipidx], x = d_x[ipidx], y = d_y[ipidx];
                  PetscReal       temp1[3] = {0, 0, 0}, temp2 = 0;
                  PetscInt        fieldA,d2,d3,f_off_r,grid_r,ipidx_g,nip_loc_r,Nfloc_r,IPf_idx_r;
#if LANDAU_DIM==2
                  PetscReal Ud[2][2], Uk[2][2], mask = (PetscAbs(vj[0]-x) < 100*PETSC_SQRT_MACHINE_EPSILON && PetscAbs(vj[1]-y) < 100*PETSC_SQRT_MACHINE_EPSILON) ? 0. : 1.;
                  LandauTensor2D(vj, x, y, Ud, Uk, mask);
#else
                  PetscReal U[3][3], z = d_z[ipidx], mask = (PetscAbs(vj[0]-x) < 100*PETSC_SQRT_MACHINE_EPSILON && PetscAbs(vj[1]-y) < 100*PETSC_SQRT_MACHINE_EPSILON && PetscAbs(vj[2]-z) < 100*PETSC_SQRT_MACHINE_EPSILON) ? 0. : 1.;
                  LandauTensor3D(vj, x, y, z, U, mask);
#endif
                  grid_r = 0;
                  while (ipidx >= d_ip_offset[grid_r+1]) grid_r++; // yuck search for grid
                  f_off_r = d_species_offset[grid_r];
                  ipidx_g = ipidx - d_ip_offset[grid_r];
                  nip_loc_r = d_numCells[grid_r]*Nq;
                  Nfloc_r = d_species_offset[grid_r+1] - d_species_offset[grid_r];
                  IPf_idx_r = d_ipf_offset[grid_r];
                  for (fieldA = 0; fieldA < Nfloc_r; ++fieldA) {
                    const PetscInt idx = IPf_idx_r + fieldA*nip_loc_r + ipidx_g;
                    temp1[0] += d_fdf_k(1,idx)*d_beta[fieldA+f_off_r]*d_invMass[fieldA+f_off_r];
                    temp1[1] += d_fdf_k(2,idx)*d_beta[fieldA+f_off_r]*d_invMass[fieldA+f_off_r];
#if LANDAU_DIM==3
                    temp1[2] += d_fdf_k(3,idx)*d_beta[fieldA+f_off_r]*d_invMass[fieldA+f_off_r];
#endif
                    temp2    += d_fdf_k(0,idx)*d_beta[fieldA+f_off_r];
                  }
                  temp1[0] *= wi;
                  temp1[1] *= wi;
#if LANDAU_DIM==3
                  temp1[2] *= wi;
#endif
                  temp2    *= wi;
#if LANDAU_DIM==2
                  for (d2 = 0; d2 < 2; d2++) {
                    for (d3 = 0; d3 < 2; ++d3) {
                      /* K = U * grad(f): g2=e: i,A */
                      ggg.gg2[d2] += Uk[d2][d3]*temp1[d3];
                      /* D = -U * (I \kron (fx)): g3=f: i,j,A */
                      ggg.gg3[d2][d3] += Ud[d2][d3]*temp2;
                    }
                  }
#else
                  for (d2 = 0; d2 < 3; ++d2) {
                    for (d3 = 0; d3 < 3; ++d3) {
                      /* K = U * grad(f): g2 = e: i,A */
                      ggg.gg2[d2] += U[d2][d3]*temp1[d3];
                      /* D = -U * (I \kron (fx)): g3 = f: i,j,A */
                      ggg.gg3[d2][d3] += U[d2][d3]*temp2;
                    }
                  }
#endif
                }, Kokkos::Sum<landau_inner_red::TensorValueType>(gg_temp));
              // add alpha and put in gg2/3
              Kokkos::parallel_for(Kokkos::ThreadVectorRange (team, (int)Nfloc), [&] (const int& fieldA) {
                  PetscInt d2,d3;
                  for (d2 = 0; d2 < dim; d2++) {
                    gg2(d2,fieldA,myQi) = gg_temp.gg2[d2]*d_alpha[fieldA+f_off];
                    for (d3 = 0; d3 < dim; d3++) {
                      gg3(d2,d3,fieldA,myQi) = -gg_temp.gg3[d2][d3]*d_alpha[fieldA+f_off]*d_invMass[fieldA+f_off];
                    }
                  }
                });
              /* add electric field term once per IP */
              Kokkos::parallel_for(Kokkos::ThreadVectorRange (team, (int)Nfloc), [&] (const int& fieldA) {
                  gg2(dim-1,fieldA,myQi) += d_Eq_m[fieldA+f_off];
                });
              Kokkos::parallel_for(Kokkos::ThreadVectorRange (team, (int)Nfloc), [=] (const int& fieldA) {
                  int d,d2,d3,dp;
                  /* Jacobian transform - g2, g3 - per thread (2D) */
                  for (d = 0; d < dim; ++d) {
                    g2(d,fieldA,myQi) = 0;
                    for (d2 = 0; d2 < dim; ++d2) {
                      g2(d,fieldA,myQi) += invJj[d*dim+d2]*gg2(d2,fieldA,myQi);
                      g3(d,d2,fieldA,myQi) = 0;
                      for (d3 = 0; d3 < dim; ++d3) {
                        for (dp = 0; dp < dim; ++dp) {
                          g3(d,d2,fieldA,myQi) += invJj[d*dim + d3]*gg3(d3,dp,fieldA,myQi)*invJj[d2*dim + dp];
                        }
                      }
                      g3(d,d2,fieldA,myQi) *= wj;
                    }
                    g2(d,fieldA,myQi) *= wj;
                  }
                });
            }); // Nq
          team.team_barrier();
          { /* assemble */
            fieldMats_scr_t s_fieldMats(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,Nb); // Only used for GPU assembly (ie, not first pass)
            idx_scr_t       s_idx(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,nfaces);
            scale_scr_t     s_scale(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,nfaces);
            for (PetscInt fieldA = 0; fieldA < Nfloc; fieldA++) {
              /* assemble */
              Kokkos::parallel_for(Kokkos::TeamThreadRange(team,0,Nb), [=] (int f) {
                  Kokkos::parallel_for(Kokkos::ThreadVectorRange(team,0,Nb), [=] (int g) {
                      PetscScalar t = 0;
                      for (int qj = 0 ; qj < Nq ; qj++) { // look at others integration points
                        const PetscReal *BJq = &d_BB[qj*Nb], *DIq = &d_DD[qj*Nb*dim];
                        for (int d = 0; d < dim; ++d) {
                          t += DIq[f*dim+d]*g2(d,fieldA,qj)*BJq[g];
                          for (int d2 = 0; d2 < dim; ++d2) {
                            t += DIq[f*dim + d]*g3(d,d2,fieldA,qj)*DIq[g*dim + d2];
                          }
                        }
                      }
                      if (elem_mat_num_cells_max_grid) { // CPU assembly
                        const PetscInt fOff = (fieldA*Nb + f)*totDim + fieldA*Nb + g;
                        d_elem_mats(grid,elem,fOff) = t;
                      } else s_fieldMats(f,g) = t;
                    });
                });
              if (!elem_mat_num_cells_max_grid) { // GPU assembly
                landau_mat_assemble (d_mat, team, s_fieldMats, s_idx, s_scale, Nb, Nq, nfaces, moffset, elem, fieldA, maps[grid]);
              }
            }
          }
        }
      });
    ierr = PetscLogGpuTimeEnd();CHKERRQ(ierr);
    ierr = PetscLogEventEnd(events[4],0,0,0,0);CHKERRQ(ierr);
  } else { // mass
    ierr = PetscLogEventBegin(events[4],0,0,0,0);CHKERRQ(ierr);
    ierr = PetscLogGpuTimeBegin();CHKERRQ(ierr);
    // #if defined(PETSC_HAVE_CUDA) || defined(PETSC_HAVE_HIP)
    //           ierr = PetscLogGpuFlops(nip_loc*(PetscLogDouble)(Nb*Nfloc*Nb*Nq*4));CHKERRQ(ierr);
    //           if (ctx->deviceType == LANDAU_CPU) PetscInfo(plex[grid], "Warning: Landau selected CPU but no support for Kokkos using CPU\n");
    // #else
    //           ierr = PetscLogFlops(nip_loc*(PetscLogDouble)(Nb*Nfloc*Nb*Nq*4));CHKERRQ(ierr);
    // #endif
    int scr_bytes = fieldMats_scr_t::shmem_size(Nq,Nq) + idx_scr_t::shmem_size(Nb,nfaces) + scale_scr_t::shmem_size(Nb,nfaces);
    ierr = PetscInfo6(plex[0], "Mass shared memory size: %d bytes in level %d conc=%D team size=%D #face=%D Nb=%D\n",scr_bytes,KOKKOS_SHARED_LEVEL,conc,team_size,nfaces,Nb);CHKERRQ(ierr);
    Kokkos::parallel_for("Mass", Kokkos::TeamPolicy<>(num_cells_tot, team_size, /* Kokkos::AUTO */ 16).set_scratch_size(KOKKOS_SHARED_LEVEL, Kokkos::PerTeam(scr_bytes)), KOKKOS_LAMBDA (const team_member team) {
        fieldMats_scr_t s_fieldMats(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,Nb);
        idx_scr_t       s_idx(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,nfaces);
        scale_scr_t     s_scale(team.team_scratch(KOKKOS_SHARED_LEVEL),Nb,nfaces);
        // find my grid
        PetscInt grid = 0, g_cell = team.league_rank();
        while (g_cell >= d_elem_offset[grid+1]) grid++; // yuck search for grid
        {
          const PetscInt moffset = d_mat_offset[grid], Nfloc = d_species_offset[grid+1]-d_species_offset[grid], totDim = Nfloc*Nq, elem = g_cell-d_elem_offset[grid];
          const PetscInt IP_idx = d_ip_offset[grid];
          for (int fieldA = 0; fieldA < Nfloc; fieldA++) {
            /* assemble */
            Kokkos::parallel_for(Kokkos::TeamThreadRange(team,0,Nb), [=] (int f) {
                Kokkos::parallel_for(Kokkos::ThreadVectorRange(team,0,Nb), [=] (int g) {
                    PetscScalar    t = 0;
                    for (int qj = 0 ; qj < Nq ; qj++) { // look at others integration points
                      const PetscReal *BJq = &d_BB[qj*Nb];
                      const PetscInt jpidx = IP_idx + qj + elem * Nq;
                      if (dim==2) {
                        t += BJq[f] * d_w_k(jpidx) * shift * BJq[g] * 2. * PETSC_PI;
                      } else {
                        t += BJq[f] * d_w_k(jpidx) * shift * BJq[g];
                      }
                    }
                    if (elem_mat_num_cells_max_grid) {
                      const PetscInt fOff = (fieldA*Nb + f)*totDim + fieldA*Nb + g;
                      d_elem_mats(grid,elem,fOff) = t;
                    } else s_fieldMats(f,g) = t;
                  });
              });
            if (!elem_mat_num_cells_max_grid) { // device assembly
              landau_mat_assemble (d_mat, team, s_fieldMats, s_idx, s_scale, Nb, Nq,nfaces, moffset, elem, fieldA, maps[grid]);
            } // else not using GPU assembly
          }
        }
      });
    ierr = PetscLogGpuTimeEnd();CHKERRQ(ierr);
    ierr = PetscLogEventEnd(events[4],0,0,0,0);CHKERRQ(ierr);
  }
  Kokkos::fence();
  if (elem_mat_num_cells_max_grid) { // CPU assembly
    Kokkos::View<PetscScalar***, Kokkos::LayoutRight>::HostMirror h_elem_mats = Kokkos::create_mirror_view(d_elem_mats);
    Kokkos::deep_copy (h_elem_mats, d_elem_mats);
    for (PetscInt grid=0 ; grid<num_grids ; grid++) {
      const PetscInt  Nfloc = a_species_offset[grid+1]-a_species_offset[grid], totDim = Nfloc*Nq;
      PetscSection    section, globalSection;
      PetscInt        cStart,cEnd;
      ierr = PetscLogEventBegin(events[5],0,0,0,0);CHKERRQ(ierr);
      ierr = DMPlexGetHeightStratum(plex[grid],0,&cStart,&cEnd);CHKERRQ(ierr);
      ierr = DMGetLocalSection(plex[grid], &section);CHKERRQ(ierr);
      ierr = DMGetGlobalSection(plex[grid], &globalSection);CHKERRQ(ierr);
      ierr = PetscLogEventEnd(events[5],0,0,0,0);CHKERRQ(ierr);
      ierr = PetscLogEventBegin(events[6],0,0,0,0);CHKERRQ(ierr);
      for (PetscInt ej = cStart ; ej < cEnd; ++ej) {
        const PetscScalar *elMat = &h_elem_mats(grid,ej-cStart,0);
        ierr = DMPlexMatSetClosure(plex[grid], section, globalSection, subJ[grid], ej, elMat, ADD_VALUES);CHKERRQ(ierr);
        if (grid==0 && ej==-1) {
          int d,f;
          PetscPrintf(PETSC_COMM_SELF,"Kokkos Element matrix %d/%d\n",1,(int)a_numCells[grid]);
          for (d = 0; d < totDim; ++d){
            for (f = 0; f < totDim; ++f) PetscPrintf(PETSC_COMM_SELF," %12.5e",  PetscRealPart(elMat[d*totDim + f]));
            PetscPrintf(PETSC_COMM_SELF,"\n");
          }
          exit(14);
        }
      }
      // transition to use of maps for a Kokkos VecGetClosure
      if (ctx->gpu_assembly) {
        if (!(a_elem_closure || a_xarray)) SETERRQ(PETSC_COMM_SELF, PETSC_ERR_PLIB, "transition in Mass");
      }
      if (!container) {   // move nest matrix to global JacP
        PetscInt          moffset = a_mat_offset[grid], nloc, nzl, colbuf[1024], row;
        const PetscInt    *cols;
        const PetscScalar *vals;
        Mat               B = subJ[grid];
        ierr = MatAssemblyBegin(B, MAT_FINAL_ASSEMBLY);CHKERRQ(ierr);
        ierr = MatAssemblyEnd(B, MAT_FINAL_ASSEMBLY);CHKERRQ(ierr);
        ierr = MatGetSize(B, &nloc, NULL);CHKERRQ(ierr);
        if (nloc != a_mat_offset[grid+1] - moffset) SETERRQ2(PetscObjectComm((PetscObject) B), PETSC_ERR_PLIB, "nloc %D != mat_offset[grid+1] - moffset = %D",nloc, a_mat_offset[grid+1] - moffset);
        for (int i=0 ; i<nloc ; i++) {
          ierr = MatGetRow(B,i,&nzl,&cols,&vals);CHKERRQ(ierr);
          if (nzl>1024) SETERRQ1(PetscObjectComm((PetscObject) B), PETSC_ERR_PLIB, "Row too big: %D",nzl);
          for (int j=0; j<nzl; j++) colbuf[j] = cols[j] + moffset;
          row = i + moffset;
          ierr = MatSetValues(JacP,1,&row,nzl,colbuf,vals,ADD_VALUES);CHKERRQ(ierr);
          ierr = MatRestoreRow(B,i,&nzl,&cols,&vals);CHKERRQ(ierr);
        }
        ierr = MatDestroy(&subJ[grid]);CHKERRQ(ierr);
      }
      ierr = PetscLogEventEnd(events[6],0,0,0,0);CHKERRQ(ierr);
    } // grids
  }
  PetscFunctionReturn(0);
}
} // extern "C"
