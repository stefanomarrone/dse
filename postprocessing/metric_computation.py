from measures import *
import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        csvfilename = sys.argv[1]
        analyser = MetricAnalyser()
        analyser.addMetric(Downtime('topevent','TopABCD','is working','is interrupted by'))
        analyser.compute(csvfilename)
        report = analyser.report()
        print(report)
    else:
        usage = sys.argv[0] + ' csvfilename element_to_analyse downstartelement upstartelement'
        print(usage)