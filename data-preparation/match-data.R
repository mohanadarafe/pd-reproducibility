library('MatchIt')
require('MatchIt')

data <- read.csv('../data/volume-data/cohortBeforeMatching')
matcher <- matchit(group ~ age+gen, data=data, method="nearest", distance="glm", replacement=F)
final_data = match.data(matcher)
write.csv(final_data, file="../data/volume-data/matchedVolumes.csv")
print(summary(matcher))
