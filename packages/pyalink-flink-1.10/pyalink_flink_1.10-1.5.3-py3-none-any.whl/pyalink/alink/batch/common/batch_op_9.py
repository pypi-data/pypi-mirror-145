# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..lazy.extract_model_info_batch_op import ExtractModelInfoBatchOp
from ..lazy.with_model_info_batch_op import WithModelInfoBatchOp
from ..lazy.with_train_info import WithTrainInfo



class VectorTrain(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.tree.Preprocessing$VectorTrain'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorTrain, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class WeightSampleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.WeightSampleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WeightSampleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRatio(self, val):
        return self._add_param('ratio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class WhereBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.WhereBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WhereBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class Word2VecPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.Word2VecPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class Word2VecTrainBatchOp(BatchOperator, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.Word2VecTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setMinCount(self, val):
        return self._add_param('minCount', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRandomWindow(self, val):
        return self._add_param('randomWindow', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setWindow(self, val):
        return self._add_param('window', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class WordCountBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.WordCountBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WordCountBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class WriteTensorToImageBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.image.WriteTensorToImageBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WriteTensorToImageBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setImageType(self, val):
        return self._add_param('imageType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.XGBoostPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.XGBoostRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostRegTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.XGBoostRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setNumRound(self, val):
        return self._add_param('numRound', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBaseScore(self, val):
        return self._add_param('baseScore', val)

    def setColSampleByLevel(self, val):
        return self._add_param('colSampleByLevel', val)

    def setColSampleByNode(self, val):
        return self._add_param('colSampleByNode', val)

    def setColSampleByTree(self, val):
        return self._add_param('colSampleByTree', val)

    def setEta(self, val):
        return self._add_param('eta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGrowPolicy(self, val):
        return self._add_param('growPolicy', val)

    def setInteractionConstraints(self, val):
        return self._add_param('interactionConstraints', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMaxBin(self, val):
        return self._add_param('maxBin', val)

    def setMaxDeltaStep(self, val):
        return self._add_param('maxDeltaStep', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinChildWeight(self, val):
        return self._add_param('minChildWeight', val)

    def setMonotoneConstraints(self, val):
        return self._add_param('monotoneConstraints', val)

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setObjective(self, val):
        return self._add_param('objective', val)

    def setProcessType(self, val):
        return self._add_param('processType', val)

    def setRefreshLeaf(self, val):
        return self._add_param('refreshLeaf', val)

    def setRunningMode(self, val):
        return self._add_param('runningMode', val)

    def setSamplingMethod(self, val):
        return self._add_param('samplingMethod', val)

    def setScalePosWeight(self, val):
        return self._add_param('scalePosWeight', val)

    def setSinglePrecisionHistogram(self, val):
        return self._add_param('singlePrecisionHistogram', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSubSample(self, val):
        return self._add_param('subSample', val)

    def setTreeMethod(self, val):
        return self._add_param('treeMethod', val)

    def setTweedieVariancePower(self, val):
        return self._add_param('tweedieVariancePower', val)

    def setUpdater(self, val):
        return self._add_param('updater', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class XGBoostTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.XGBoostTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setNumRound(self, val):
        return self._add_param('numRound', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBaseScore(self, val):
        return self._add_param('baseScore', val)

    def setColSampleByLevel(self, val):
        return self._add_param('colSampleByLevel', val)

    def setColSampleByNode(self, val):
        return self._add_param('colSampleByNode', val)

    def setColSampleByTree(self, val):
        return self._add_param('colSampleByTree', val)

    def setEta(self, val):
        return self._add_param('eta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGrowPolicy(self, val):
        return self._add_param('growPolicy', val)

    def setInteractionConstraints(self, val):
        return self._add_param('interactionConstraints', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMaxBin(self, val):
        return self._add_param('maxBin', val)

    def setMaxDeltaStep(self, val):
        return self._add_param('maxDeltaStep', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinChildWeight(self, val):
        return self._add_param('minChildWeight', val)

    def setMonotoneConstraints(self, val):
        return self._add_param('monotoneConstraints', val)

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setObjective(self, val):
        return self._add_param('objective', val)

    def setProcessType(self, val):
        return self._add_param('processType', val)

    def setRefreshLeaf(self, val):
        return self._add_param('refreshLeaf', val)

    def setRunningMode(self, val):
        return self._add_param('runningMode', val)

    def setSamplingMethod(self, val):
        return self._add_param('samplingMethod', val)

    def setScalePosWeight(self, val):
        return self._add_param('scalePosWeight', val)

    def setSinglePrecisionHistogram(self, val):
        return self._add_param('singlePrecisionHistogram', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSubSample(self, val):
        return self._add_param('subSample', val)

    def setTreeMethod(self, val):
        return self._add_param('treeMethod', val)

    def setUpdater(self, val):
        return self._add_param('updater', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class Zipped2KObjectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.recommendation.Zipped2KObjectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Zipped2KObjectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setObjectCol(self, val):
        return self._add_param('objectCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setInfoCols(self, val):
        return self._add_param('infoCols', val)

