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
    tempSet = []
    inputFile = open(pageLinks,'r')

    # finding # of inlinks and # of pages.
    for line in inputFile.readlines():
        line = line.split()
        for val in line[1:]:
            if val not in tempSet:
                tempSet.append(val)
                if outlinks.has_key(val):
                    outlinks[val] += 1
                else:
                    outlinks[val] = 1
        inlinks[line[0]] = tempSet
        tempSet = []
        pages.append(line[0])


    # initial page rank value for each page
    initialPRVal = float(1)/float(len(pages))
    for page in pages:
        pageRank[page] = float(1)/float(len(pages))

   # finding the # of sink nodes
    sinkNodes = list(set(pages).difference(set(outlinks.keys())))

    sources = 0
    sources = countSources(inlinks,sources)

    writeOutput(str(sources/float(len(pages))),'Sources Proportions','proportions')
    writeOutput(str(len(sinkNodes)/float(len(pages))),'SinkNode Proportions','proportions')

    computePageRank(inlinks,outlinks,pageRank,sinkNodes,sources,initialPRVal)

def computePageRank(inlinks,outlinks,pageRank,sinkNodes,sources,initialPRVal):

    # initial perplexity value
    perplexity = float(0)
    inlinkLen = float(len(inlinks))
    counter = 0
    i = 0
    file = open('Output/Perplexity', 'w')
    while(i<=3):
        sinkPR = 0
        newPerplexity = float(computePerplexity(pageRank))
        if math.fabs(newPerplexity - perplexity) < 1:
            i += 1
        else:
            i = 0
        perplexity = newPerplexity
        file.write('Iterations : '+ str(counter) +" : " + str(perplexity) +"\n")
        for page in sinkNodes:
            sinkPR += pageRank.get(page)
        for page in inlinks.keys():
            newPR[page] = float(1.0 - d) / inlinkLen
            newPR[page] = newPR[page] + float(d * sinkPR) / inlinkLen
            for q in inlinks[page]:
                newPR[page] += float(d*pageRank.get(q)) / outlinks.get(q)
        for page in newPR.keys():
            pageRank[page] = newPR.get(page)

        counter += 1

    file.close()

    prCounter = 0
    for val in newPR.values():
        if val < initialPRVal:
            prCounter += 1

    writeOutput(str(prCounter/float(len(inlinks))),'Page Rank Proportions','proportions')
    topRank(pageRank)
    topInlinks(inlinks)

def countSources(inlinks,sources):
    for val in inlinks.values():
        if len(val) == 0:
            sources += 1

    return sources

def topRank(pageRank):
    sortPageRank = sorted(pageRank.iteritems(), key= operator.itemgetter(1),reverse=True)
    writeOutput(sortPageRank,"TopRankPages",'')

def topInlinks(inlinks):
    topInlinkRank = {}
    for page in inlinks.keys():
        topInlinkRank[page] = len(inlinks.get(page))
    inlinkRank = sorted(topInlinkRank.iteritems(),key=operator.itemgetter(1),reverse=True)
    type(inlinkRank)
    writeOutput(inlinkRank,"TopInlinks",'')

def computePerplexity(pageRank):
    h = 0
    for page in pageRank.keys():
        h += pageRank[page]*math.log(1/pageRank[page],2)
    return 2**h

def writeOutput(finalResult,type,flag):

    if flag == 'proportions':
        file = open('Output/'+type, 'w')
        file.write("proportion : " + finalResult)
    else:
        file = open('Output/Results-'+ type,'w')
        for i in range(50):
            file.write(str(finalResult[i][0]) + " : " +  str(finalResult[i][1]) +"\n")
    file.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])