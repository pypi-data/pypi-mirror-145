#include <petsc/private/dmpleximpl.h>   /*I      "petscdmplex.h"   I*/
#include <petscblaslapack.h>

PetscErrorCode DMPlexP1FieldCreate_Private(DM dm, PetscInt f, PetscInt size, Vec *metric)
{
  MPI_Comm       comm;
  PetscErrorCode ierr;
  PetscFE        fe;
  PetscInt       dim;

  PetscFunctionBegin;

  /* Extract metadata from dm */
  ierr = PetscObjectGetComm((PetscObject) dm, &comm);CHKERRQ(ierr);
  ierr = DMGetDimension(dm, &dim);CHKERRQ(ierr);

  /* Create a P1 field of the requested size */
  ierr = PetscFECreateLagrange(comm, dim, size, PETSC_TRUE, 1, PETSC_DETERMINE, &fe);CHKERRQ(ierr);
  ierr = DMSetField(dm, f, NULL, (PetscObject)fe);CHKERRQ(ierr);
  ierr = DMCreateDS(dm);CHKERRQ(ierr);
  ierr = PetscFEDestroy(&fe);CHKERRQ(ierr);
  ierr = DMCreateLocalVector(dm, metric);CHKERRQ(ierr);

  PetscFunctionReturn(0);
}

/*
  DMPlexMetricCreate - Create a Riemannian metric field

  Input parameters:
+ dm     - The DM
- f      - The field number to use

  Output parameter:
. metric - The metric

  Level: beginner

  Note: It is assumed that the DM is comprised of simplices.

.seealso: DMPlexMetricCreateUniform(), DMPlexMetricCreateIsotropic()
*/
PetscErrorCode DMPlexMetricCreate(DM dm, PetscInt f, Vec *metric)
{
  PetscErrorCode ierr;
  PetscInt       coordDim, Nd;

  PetscFunctionBegin;
  ierr = DMGetCoordinateDim(dm, &coordDim);CHKERRQ(ierr);
  Nd = coordDim*coordDim;
  ierr = DMPlexP1FieldCreate_Private(dm, f, Nd, metric);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

typedef struct {
  PetscReal scaling;  /* Scaling for uniform metric diagonal */
} DMPlexMetricUniformCtx;

static PetscErrorCode diagonal(PetscInt dim, PetscReal time, const PetscReal x[], PetscInt Nc, PetscScalar *u, void *ctx)
{
  DMPlexMetricUniformCtx *user = (DMPlexMetricUniformCtx*)ctx;
  PetscInt                i, j;

  for (i = 0; i < dim; ++i) {
    for (j = 0; j < dim; ++j) {
      if (i == j) u[i+dim*j] = user->scaling;
      else u[i+dim*j] = 0.0;
    }
  }
  return 0;
}

/*
  DMPlexMetricCreateUniform - Construct a uniform isotropic metric

  Input parameters:
+ dm     - The DM
. f      - The field number to use
- alpha  - Scaling parameter for the diagonal

  Output parameter:
. metric - The uniform metric

  Level: beginner

  Note: It is assumed that the DM is comprised of simplices.

.seealso: DMPlexMetricCreate(), DMPlexMetricCreateIsotropic()
*/
PetscErrorCode DMPlexMetricCreateUniform(DM dm, PetscInt f, PetscReal alpha, Vec *metric)
{
  DMPlexMetricUniformCtx user;
  PetscErrorCode       (*funcs[1])(PetscInt, PetscReal, const PetscReal [], PetscInt, PetscScalar *, void *);
  PetscErrorCode         ierr;
  void                  *ctxs[1];

  PetscFunctionBegin;
  ierr = DMPlexMetricCreate(dm, f, metric);CHKERRQ(ierr);
  if (!alpha) SETERRQ(PETSC_COMM_SELF, PETSC_ERR_ARG_WRONG, "Uniform metric scaling is undefined");
  if (alpha < 1.0e-30) SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_ARG_WRONG, "Uniform metric scaling %e should be positive", alpha);
  else user.scaling = alpha;
  funcs[0] = diagonal;
  ctxs[0] = &user;
  ierr = DMProjectFunctionLocal(dm, 0.0, funcs, ctxs, INSERT_ALL_VALUES, *metric);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

/*
  DMPlexMetricCreateIsotropic - Construct an isotropic metric from an error indicator

  Input parameters:
+ dm        - The DM
. f         - The field number to use
- indicator - The error indicator

  Output parameter:
. metric    - The isotropic metric

  Level: beginner

  Notes:

  It is assumed that the DM is comprised of simplices.

  The indicator needs to be a scalar field defined at *vertices*.

.seealso: DMPlexMetricCreate(), DMPlexMetricCreateUniform()
*/
PetscErrorCode DMPlexMetricCreateIsotropic(DM dm, PetscInt f, Vec indicator, Vec *metric)
{
  DM                 dmIndi;
  PetscErrorCode     ierr;
  PetscInt           dim, d, vStart, vEnd, v;
  const PetscScalar *indi;
  PetscScalar       *met;

  PetscFunctionBegin;
  ierr = DMGetDimension(dm, &dim);CHKERRQ(ierr);
  ierr = DMPlexMetricCreate(dm, f, metric);CHKERRQ(ierr);
  ierr = DMPlexGetDepthStratum(dm, 0, &vStart, &vEnd);CHKERRQ(ierr);
  ierr = VecGetArrayRead(indicator, &indi);CHKERRQ(ierr);
  ierr = VecGetArrayWrite(*metric, &met);CHKERRQ(ierr);
  ierr = VecGetDM(indicator, &dmIndi);CHKERRQ(ierr);
  for (v = vStart; v < vEnd; ++v) {
    PetscScalar *vindi, *vmet;
    ierr = DMPlexPointLocalRead(dmIndi, v, indi, &vindi);CHKERRQ(ierr);
    ierr = DMPlexPointLocalRef(dm, v, met, &vmet);CHKERRQ(ierr);
    for (d = 0; d < dim; ++d) vmet[d*(dim+1)] = vindi[0];
  }
  ierr = VecRestoreArrayWrite(*metric, &met);CHKERRQ(ierr);
  ierr = VecRestoreArrayRead(indicator, &indi);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

static PetscErrorCode DMPlexMetricModify_Private(PetscInt dim, PetscReal h_min, PetscReal h_max, PetscReal a_max, PetscScalar Mp[])
{
  PetscErrorCode ierr;
  PetscInt       i, j, k;
  PetscReal     *eigs, max_eig, l_min = 1.0/(h_max*h_max), l_max = 1.0/(h_min*h_min), la_min = 1.0/(a_max*a_max);
  PetscScalar   *Mpos;

  PetscFunctionBegin;
  ierr = PetscMalloc2(dim*dim, &Mpos, dim, &eigs);CHKERRQ(ierr);

  /* Symmetrize */
  for (i = 0; i < dim; ++i) {
    Mpos[i*dim+i] = Mp[i*dim+i];
    for (j = i+1; j < dim; ++j) {
      Mpos[i*dim+j] = 0.5*(Mp[i*dim+j] + Mp[j*dim+i]);
      Mpos[j*dim+i] = Mpos[i*dim+j];
    }
  }

  /* Compute eigendecomposition */
  {
    PetscScalar  *work;
    PetscBLASInt lwork;

    lwork = 5*dim;
    ierr = PetscMalloc1(5*dim, &work);CHKERRQ(ierr);
    {
      PetscBLASInt lierr;
      PetscBLASInt nb;

      ierr = PetscBLASIntCast(dim, &nb);CHKERRQ(ierr);
      ierr = PetscFPTrapPush(PETSC_FP_TRAP_OFF);CHKERRQ(ierr);
#if defined(PETSC_USE_COMPLEX)
      {
        PetscReal *rwork;
        ierr = PetscMalloc1(3*dim, &rwork);CHKERRQ(ierr);
        PetscStackCallBLAS("LAPACKsyev",LAPACKsyev_("V","U",&nb,Mpos,&nb,eigs,work,&lwork,rwork,&lierr));
        ierr = PetscFree(rwork);CHKERRQ(ierr);
      }
#else
      PetscStackCallBLAS("LAPACKsyev",LAPACKsyev_("V","U",&nb,Mpos,&nb,eigs,work,&lwork,&lierr));
#endif
      if (lierr) SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_LIB, "Error in LAPACK routine %d", (int) lierr);
      ierr = PetscFPTrapPop();CHKERRQ(ierr);
    }
    ierr = PetscFree(work);CHKERRQ(ierr);
  }

  /* Reflect to positive orthant and enforce maximum and minimum size */
  max_eig = 0.0;
  for (i = 0; i < dim; ++i) {
    eigs[i] = PetscMin(l_max, PetscMax(l_min, PetscAbsReal(eigs[i])));
    max_eig = PetscMax(eigs[i], max_eig);
  }

  /* Enforce maximum anisotropy */
  for (i = 0; i < dim; ++i) {
    if (a_max > 1.0) eigs[i] = PetscMax(eigs[i], max_eig*la_min);
  }

  /* Reconstruct Hessian */
  for (i = 0; i < dim; ++i) {
    for (j = 0; j < dim; ++j) {
      Mp[i*dim+j] = 0.0;
      for (k = 0; k < dim; ++k) {
        Mp[i*dim+j] += Mpos[k*dim+i] * eigs[k] * Mpos[k*dim+j];
      }
    }
  }
  ierr = PetscFree2(Mpos, eigs);CHKERRQ(ierr);

  PetscFunctionReturn(0);
}

/*
  DMPlexMetricEnforceSPD - Enforce symmetric positive-definiteness of a metric

  Input parameters:
+ dm            - The DM
. restrictSizes - Should maximum/minimum metric magnitudes and anisotropy be enforced?
- metric        - The metric

  Output parameter:
. metric        - The metric

  Level: beginner

.seealso: DMPlexMetricNormalize(), DMPlexMetricIntersection()
*/
PetscErrorCode DMPlexMetricEnforceSPD(DM dm, PetscBool restrictSizes, Vec metric)
{
  DMPlexMetricCtx *user;
  PetscErrorCode   ierr;
  PetscInt         dim, vStart, vEnd, v;
  PetscScalar     *met;
  PetscReal        h_min = 1.0e-30, h_max = 1.0e+30, a_max = 0.0;

  PetscFunctionBegin;

  /* Extract metadata from dm */
  ierr = DMGetDimension(dm, &dim);CHKERRQ(ierr);
  ierr = DMGetApplicationContext(dm, (void**)&user);CHKERRQ(ierr);
  if (restrictSizes) {
    if (user->h_max > h_min) h_max = PetscMin(h_max, user->h_max);
    if (user->h_min > 0.0) h_min = PetscMax(h_min, user->h_min);
    if (user->a_max > 1.0) a_max = user->a_max;
  }

  /* Enforce SPD */
  ierr = DMPlexGetDepthStratum(dm, 0, &vStart, &vEnd);CHKERRQ(ierr);
  ierr = VecGetArray(metric, &met);CHKERRQ(ierr);
  for (v = vStart; v < vEnd; ++v) {
    PetscScalar *vmet;
    ierr = DMPlexPointLocalRef(dm, v, met, &vmet);CHKERRQ(ierr);
    ierr = DMPlexMetricModify_Private(dim, h_min, h_max, a_max, vmet);CHKERRQ(ierr);
  }
  ierr = VecRestoreArray(metric, &met);CHKERRQ(ierr);

  PetscFunctionReturn(0);
}

static void detMFunc(PetscInt dim, PetscInt Nf, PetscInt NfAux,
                     const PetscInt uOff[], const PetscInt uOff_x[], const PetscScalar u[], const PetscScalar u_t[], const PetscScalar u_x[],
                     const PetscInt aOff[], const PetscInt aOff_x[], const PetscScalar a[], const PetscScalar a_t[], const PetscScalar a_x[],
                     PetscReal t, const PetscReal x[], PetscInt numConstants, const PetscScalar constants[], PetscScalar f0[])
{
  const PetscScalar p = constants[0];
  PetscReal         detH = 0.0;

  if      (dim == 2) DMPlex_Det2D_Scalar_Internal(&detH, u);
  else if (dim == 3) DMPlex_Det3D_Scalar_Internal(&detH, u);
  f0[0] = PetscPowReal(detH, p/(2.0*p + dim));
}

/*
  DMPlexMetricNormalize - Apply L-p normalization to a metric

  Input parameters:
+ dm            - The DM
. metricIn      - The unnormalized metric
- restrictSizes - Should maximum/minimum metric magnitudes and anisotropy be enforced?

  Output parameter:
. metricOut     - The normalized metric

  Level: beginner

.seealso: DMPlexMetricEnforceSPD(), DMPlexMetricIntersection()
*/
PetscErrorCode DMPlexMetricNormalize(DM dm, Vec metricIn, PetscBool restrictSizes, Vec *metricOut)
{
  DMPlexMetricCtx *user;
  MPI_Comm         comm;
  PetscDS          ds;
  PetscErrorCode   ierr;
  PetscInt         dim, Nd, vStart, vEnd, v, i;
  PetscScalar     *met, integral, constants[1];
  PetscReal        p, h_min = 1.0e-30, h_max = 1.0e+30, a_max = 0.0, factGlob, target;

  PetscFunctionBegin;

  /* Extract metadata from dm */
  ierr = PetscObjectGetComm((PetscObject) dm, &comm);CHKERRQ(ierr);
  ierr = DMGetDimension(dm, &dim);CHKERRQ(ierr);
  Nd = dim*dim;
  ierr = DMPlexGetDepthStratum(dm, 0, &vStart, &vEnd);CHKERRQ(ierr);
  ierr = DMGetApplicationContext(dm, (void**)&user);CHKERRQ(ierr);
  if (restrictSizes && user->restrictAnisotropyFirst && user->a_max > 1.0) a_max = user->a_max;
  if (PetscAbsReal(user->p) >= 1.0) p = user->p;
  else SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_ARG_WRONG, "Metric normalization order %f should be greater than one.", user->p);
  constants[0] = p;
  if (user->targetComplexity > 0.0) target = user->targetComplexity;
  else SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_ARG_WRONG, "Target metric complexity %f should be positive.", user->targetComplexity);

  /* Set up metric and ensure it is SPD */
  ierr = DMPlexMetricCreate(dm, 0, metricOut);CHKERRQ(ierr);
  ierr = VecCopy(metricIn, *metricOut);CHKERRQ(ierr);
  ierr = DMPlexMetricEnforceSPD(dm, PETSC_FALSE, *metricOut);CHKERRQ(ierr);

  /* Compute global normalization factor */
  ierr = DMGetDS(dm, &ds);CHKERRQ(ierr);
  ierr = PetscDSSetConstants(ds, 1, constants);CHKERRQ(ierr);
  ierr = PetscDSSetObjective(ds, 0, detMFunc);CHKERRQ(ierr);
  ierr = DMPlexComputeIntegralFEM(dm, *metricOut, &integral, NULL);CHKERRQ(ierr);
  factGlob = PetscPowReal(target/PetscRealPart(integral), 2.0/dim);

  /* Apply local scaling */
  a_max = 0.0;
  if (restrictSizes) {
    if (user->h_max > h_min) h_max = PetscMin(h_max, user->h_max);
    if (user->h_min > 0.0) h_min = PetscMax(h_min, user->h_min);
    if (!user->restrictAnisotropyFirst && user->a_max > 1.0) a_max = user->a_max;
  }
  ierr = VecGetArray(*metricOut, &met);CHKERRQ(ierr);
  for (v = vStart; v < vEnd; ++v) {
    PetscScalar       *Mp;
    PetscReal          detM, fact;

    ierr = DMPlexPointLocalRef(dm, v, met, &Mp);CHKERRQ(ierr);
    if      (dim == 2) DMPlex_Det2D_Scalar_Internal(&detM, Mp);
    else if (dim == 3) DMPlex_Det3D_Scalar_Internal(&detM, Mp);
    else SETERRQ1(comm, PETSC_ERR_SUP, "Dimension %d not supported", dim);
    fact = factGlob * PetscPowReal(PetscAbsReal(detM), -1.0/(2*p+dim));
    for (i = 0; i < Nd; ++i) Mp[i] *= fact;
    if (restrictSizes) { ierr = DMPlexMetricModify_Private(dim, h_min, h_max, a_max, Mp);CHKERRQ(ierr); }
  }
  ierr = VecRestoreArray(*metricOut, &met);CHKERRQ(ierr);

  PetscFunctionReturn(0);
}

/*
  DMPlexMetricAverage - Compute the average of a list of metrics

  Input Parameter:
+ dm         - The DM
. numMetrics - The number of metrics to be averaged
. weights    - Weights for the average
- metrics    - The metrics to be averaged

  Output Parameter:
. metricAvg  - The averaged metric

  Level: beginner

  Notes:
  The weights should sum to unity.

  If weights are not provided then an unweighted average is used.

.seealso: DMPlexMetricAverage2(), DMPlexMetricAverage3(), DMPlexMetricIntersection()
*/
PetscErrorCode DMPlexMetricAverage(DM dm, PetscInt numMetrics, PetscReal weights[], Vec metrics[], Vec *metricAvg)
{
  PetscBool      haveWeights = PETSC_TRUE;
  PetscErrorCode ierr;
  PetscInt       i;
  PetscReal      sum = 0.0, tol = 1.0e-10;

  PetscFunctionBegin;
  if (numMetrics < 1) { SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_ARG_OUTOFRANGE, "Cannot average %d < 1 metrics", numMetrics); }
  ierr = DMPlexMetricCreate(dm, 0, metricAvg);CHKERRQ(ierr);
  ierr = VecSet(*metricAvg, 0.0);CHKERRQ(ierr);

  /* Default to the unweighted case */
  if (!weights) {
    ierr = PetscMalloc1(numMetrics, &weights);CHKERRQ(ierr);
    haveWeights = PETSC_FALSE;
    for (i = 0; i < numMetrics; ++i) {weights[i] = 1.0/numMetrics; }
  }

  /* Check weights sum to unity */
  for (i = 0; i < numMetrics; ++i) { sum += weights[i]; }
  if (PetscAbsReal(sum - 1) > tol) { SETERRQ(PETSC_COMM_SELF, PETSC_ERR_ARG_OUTOFRANGE, "Weights do not sum to unity"); }

  /* Compute metric average */
  for (i = 0; i < numMetrics; ++i) { ierr = VecAXPY(*metricAvg, weights[i], metrics[i]);CHKERRQ(ierr); }
  if (!haveWeights) {ierr = PetscFree(weights); }
  PetscFunctionReturn(0);
}

/*
  DMPlexMetricAverage2 - Compute the unweighted average of two metrics

  Input Parameter:
+ dm         - The DM
. metric1    - The first metric to be averaged
- metric2    - The second metric to be averaged

  Output Parameter:
. metricAvg  - The averaged metric

  Level: beginner

.seealso: DMPlexMetricAverage(), DMPlexMetricAverage3()
*/
PetscErrorCode DMPlexMetricAverage2(DM dm, Vec metric1, Vec metric2, Vec *metricAvg)
{
  PetscErrorCode ierr;
  PetscReal      weights[2] = {0.5, 0.5};
  Vec            metrics[2] = {metric1, metric2};

  PetscFunctionBegin;
  ierr = DMPlexMetricAverage(dm, 2, weights, metrics, metricAvg);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

/*
  DMPlexMetricAverage3 - Compute the unweighted average of three metrics

  Input Parameter:
+ dm         - The DM
. metric1    - The first metric to be averaged
. metric2    - The second metric to be averaged
- metric3    - The third metric to be averaged

  Output Parameter:
. metricAvg  - The averaged metric

  Level: beginner

.seealso: DMPlexMetricAverage(), DMPlexMetricAverage2()
*/
PetscErrorCode DMPlexMetricAverage3(DM dm, Vec metric1, Vec metric2, Vec metric3, Vec *metricAvg)
{
  PetscErrorCode ierr;
  PetscReal      weights[3] = {1.0/3.0, 1.0/3.0, 1.0/3.0};
  Vec            metrics[3] = {metric1, metric2, metric3};

  PetscFunctionBegin;
  ierr = DMPlexMetricAverage(dm, 3, weights, metrics, metricAvg);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

static PetscErrorCode DMPlexMetricIntersection_Private(PetscInt dim, PetscScalar M1[], PetscScalar M2[])
{
  PetscErrorCode ierr;
  PetscInt       i, j, k, l, m;
  PetscReal     *evals, *evals1;
  PetscScalar   *evecs, *sqrtM1, *isqrtM1;

  PetscFunctionBegin;
  ierr = PetscMalloc5(dim*dim, &evecs, dim*dim, &sqrtM1, dim*dim, &isqrtM1, dim, &evals, dim, &evals1);CHKERRQ(ierr);
  for (i = 0; i < dim; ++i) {
    for (j = 0; j < dim; ++j) {
      evecs[i*dim+j] = M1[i*dim+j];
    }
  }
  {
    PetscScalar *work;
    PetscBLASInt lwork;

    lwork = 5*dim;
    ierr = PetscMalloc1(5*dim, &work);CHKERRQ(ierr);
    {
      PetscBLASInt lierr, nb;
      PetscReal    sqrtk;

      /* Compute eigendecomposition of M1 */
      ierr = PetscBLASIntCast(dim, &nb);CHKERRQ(ierr);
      ierr = PetscFPTrapPush(PETSC_FP_TRAP_OFF);CHKERRQ(ierr);
#if defined(PETSC_USE_COMPLEX)
      {
        PetscReal *rwork;
        ierr = PetscMalloc1(3*dim, &rwork);CHKERRQ(ierr);
        PetscStackCallBLAS("LAPACKsyev", LAPACKsyev_("V", "U", &nb, evecs, &nb, evals1, work, &lwork, rwork, &lierr));
        ierr = PetscFree(rwork);CHKERRQ(ierr);
      }
#else
      PetscStackCallBLAS("LAPACKsyev", LAPACKsyev_("V", "U", &nb, evecs, &nb, evals1, work, &lwork, &lierr));
#endif
      if (lierr) SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_LIB, "Error in LAPACK routine %d", (int) lierr);
      ierr = PetscFPTrapPop();

      /* Compute square root and reciprocal */
      for (i = 0; i < dim; ++i) {
        for (j = 0; j < dim; ++j) {
          sqrtM1[i*dim+j] = 0.0;
          isqrtM1[i*dim+j] = 0.0;
          for (k = 0; k < dim; ++k) {
            sqrtk = PetscSqrtReal(evals1[k]);
            sqrtM1[i*dim+j] += evecs[k*dim+i] * sqrtk * evecs[k*dim+j];
            isqrtM1[i*dim+j] += evecs[k*dim+i] * (1.0/sqrtk) * evecs[k*dim+j];
          }
        }
      }

      /* Map into the space spanned by the eigenvectors of M1 */
      for (i = 0; i < dim; ++i) {
        for (j = 0; j < dim; ++j) {
          evecs[i*dim+j] = 0.0;
          for (k = 0; k < dim; ++k) {
            for (l = 0; l < dim; ++l) {
              evecs[i*dim+j] += isqrtM1[i*dim+k] * M2[l*dim+k] * isqrtM1[j*dim+l];
            }
          }
        }
      }

      /* Compute eigendecomposition */
      ierr = PetscFPTrapPush(PETSC_FP_TRAP_OFF);CHKERRQ(ierr);
#if defined(PETSC_USE_COMPLEX)
      {
        PetscReal *rwork;
        ierr = PetscMalloc1(3*dim, &rwork);CHKERRQ(ierr);
        PetscStackCallBLAS("LAPACKsyev", LAPACKsyev_("V", "U", &nb, evecs, &nb, evals, work, &lwork, rwork, &lierr));
        ierr = PetscFree(rwork);CHKERRQ(ierr);
      }
#else
      PetscStackCallBLAS("LAPACKsyev", LAPACKsyev_("V", "U", &nb, evecs, &nb, evals, work, &lwork, &lierr));
#endif
      if (lierr) SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_LIB, "Error in LAPACK routine %d", (int) lierr);
      ierr = PetscFPTrapPop();

      /* Modify eigenvalues */
      for (i = 0; i < dim; ++i) evals[i] = PetscMin(evals[i], evals1[i]);

      /* Map back to get the intersection */
      for (i = 0; i < dim; ++i) {
        for (j = 0; j < dim; ++j) {
          M2[i*dim+j] = 0.0;
          for (k = 0; k < dim; ++k) {
            for (l = 0; l < dim; ++l) {
              for (m = 0; m < dim; ++m) {
                M2[i*dim+j] += sqrtM1[i*dim+k] * evecs[l*dim+k] * evals[l] * evecs[l*dim+m] * sqrtM1[j*dim+m];
              }
            }
          }
        }
      }
    }
    ierr = PetscFree(work);CHKERRQ(ierr);
  }
  ierr = PetscFree5(evecs, sqrtM1, isqrtM1, evals, evals1);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

/*
  DMPlexMetricIntersection - Compute the intersection of a list of metrics

  Input Parameter:
+ dm         - The DM
. numMetrics - The number of metrics to be intersected
- metrics    - The metrics to be intersected

  Output Parameter:
. metricInt  - The intersected metric

  Level: beginner

  Notes:

  The intersection of a list of metrics has the maximal ellipsoid which fits within the ellipsoids of the component metrics.

  The implementation used here is only consistent with the maximal ellipsoid definition in the case numMetrics = 2.

.seealso: DMPlexMetricIntersection2(), DMPlexMetricIntersection3(), DMPlexMetricAverage()
*/
PetscErrorCode DMPlexMetricIntersection(DM dm, PetscInt numMetrics, Vec metrics[], Vec *metricInt)
{
  PetscErrorCode ierr;
  PetscInt       dim, vStart, vEnd, v, i;
  PetscScalar   *met, *meti, *M, *Mi;

  PetscFunctionBegin;
  if (numMetrics < 1) { SETERRQ1(PETSC_COMM_SELF, PETSC_ERR_ARG_OUTOFRANGE, "Cannot intersect %d < 1 metrics", numMetrics); }

  /* Extract metadata from dm */
  ierr = DMGetDimension(dm, &dim);CHKERRQ(ierr);
  ierr = DMPlexMetricCreate(dm, 0, metricInt);CHKERRQ(ierr);
  ierr = DMPlexGetDepthStratum(dm, 0, &vStart, &vEnd);CHKERRQ(ierr);

  /* Copy over the first metric */
  ierr = VecCopy(metrics[0], *metricInt);CHKERRQ(ierr);

  /* Intersect subsequent metrics in turn */
  if (numMetrics > 1) {
    ierr = VecGetArray(*metricInt, &met);CHKERRQ(ierr);
    for (i = 1; i < numMetrics; ++i) {
      ierr = VecGetArray(metrics[i], &meti);CHKERRQ(ierr);
      for (v = vStart; v < vEnd; ++v) {
        ierr = DMPlexPointLocalRef(dm, v, met, &M);CHKERRQ(ierr);
        ierr = DMPlexPointLocalRef(dm, v, meti, &Mi);CHKERRQ(ierr);
        ierr = DMPlexMetricIntersection_Private(dim, Mi, M);CHKERRQ(ierr);
      }
      ierr = VecRestoreArray(metrics[i], &meti);CHKERRQ(ierr);
    }
    ierr = VecRestoreArray(*metricInt, &met);CHKERRQ(ierr);
  }

  PetscFunctionReturn(0);
}

/*
  DMPlexMetricIntersection2 - Compute the intersection of two metrics

  Input Parameter:
+ dm        - The DM
. metric1   - The first metric to be intersected
- metric2   - The second metric to be intersected

  Output Parameter:
. metricInt - The intersected metric

  Level: beginner

.seealso: DMPlexMetricIntersection(), DMPlexMetricIntersection3()
*/
PetscErrorCode DMPlexMetricIntersection2(DM dm, Vec metric1, Vec metric2, Vec *metricInt)
{
  PetscErrorCode ierr;
  Vec            metrics[2] = {metric1, metric2};

  PetscFunctionBegin;
  ierr = DMPlexMetricIntersection(dm, 2, metrics, metricInt);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

/*
  DMPlexMetricIntersection3 - Compute the intersection of three metrics

  Input Parameter:
+ dm        - The DM
. metric1   - The first metric to be intersected
. metric2   - The second metric to be intersected
- metric3   - The third metric to be intersected

  Output Parameter:
. metricInt - The intersected metric

  Level: beginner

.seealso: DMPlexMetricIntersection(), DMPlexMetricIntersection2()
*/
PetscErrorCode DMPlexMetricIntersection3(DM dm, Vec metric1, Vec metric2, Vec metric3, Vec *metricInt)
{
  PetscErrorCode ierr;
  Vec            metrics[3] = {metric1, metric2, metric3};

  PetscFunctionBegin;
  ierr = DMPlexMetricIntersection(dm, 3, metrics, metricInt);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}
