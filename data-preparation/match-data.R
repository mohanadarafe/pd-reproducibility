library('MatchIt')
require('MatchIt')

data <- read.csv('../data/volume-data/preMatchVolumes.csv')
matcher <- matchit(group ~ age+gen+initialHY, data=data, method="nearest", distance="glm", replacement=F)
final_data = match.data(matcher)
write.csv(final_data, file="../data/volume-data/matchedVolumes.csv")
print(summary(matcher))
