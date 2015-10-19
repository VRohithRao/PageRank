__author__ = 'Rohith Vallu'
import sys
import math as math
import operator

# global variables
newPR = {}
d = 0.85

# main method
def main(pageLinks):

    pageRank = {}
    parseData(pageLinks,pageRank)

# method to parse the input file to get inlinks, outlinks and sink nodes
def parseData(pageLinks,pageRank):

    inlinks = {}
    outlinks = {}
    pages = []

    inputFile = open(pageLinks,'r')

    # finding # of inlinks and # of pages.
    for line in inputFile.readlines():
        line = line.split()
        inlinks[line[0]] = line[1:]
        pages.append(line[0])

    # initial page rank value for each page
    for page in pages:
        pageRank[page] = float(1)/float(len(pages))

    # finding the # of outlinks for each page
    for page in inlinks.keys():
        for outLink in inlinks[page]:
            if outlinks.has_key(outLink):
                outlinks[outLink] += 1
            else:
                outlinks[outLink] = 1

    # finding the # of sink nodes
    sinkNodes = list(set(pages).difference(set(outlinks.keys())))

    computePageRank(inlinks,outlinks,pageRank,sinkNodes,1)
    computePageRank(inlinks,outlinks,pageRank,sinkNodes,10)
    computePageRank(inlinks,outlinks,pageRank,sinkNodes,100)


def computePageRank(inlinks,outlinks,pageRank,sinkNodes,i):
    # initial perplexity value
    perplexity = float(0)
    inlinkLen = float(len(inlinks))
    counter = 0
    j = 1
    while(j<=i):
        sinkPR = 0
        for page in sinkNodes:
            sinkPR += pageRank.get(page)
        for page in inlinks.keys():
            newPR[page] = float(1.0 - d) / inlinkLen
            newPR[page] = newPR[page] + float(d * sinkPR) / inlinkLen
            for q in inlinks[page]:
                newPR[page] += float(d*pageRank.get(q)) / outlinks.get(q)
        for page in newPR.keys():
            pageRank[page] = newPR.get(page)

        j += 1
        counter += 1

    print(counter)

    writeOutput(pageRank,i)

def writeOutput(finalResult,i):
    file = open('Output/iterations-'+str(i),'w')
    for key,val in finalResult.items():
        file.write(str(key) + ":" + str(val) +"\n")

    file.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])