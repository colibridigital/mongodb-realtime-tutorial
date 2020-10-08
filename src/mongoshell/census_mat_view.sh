# MongoDB Materialised View

# define on demand view
calculatePopulationCounts = function() {
   db.uspopulation.aggregate( [
      {$group: {_id: {year: "$year", statistical_area_state: "$statistical_area_state"},
        state_area_total_population: {$sum: "$details.total_population"},
        state_area_total_population_male: {$sum: "$details.total_population_male"},
        state_area_total_population_female: {$sum: "$details.total_population_female"}}},
      {$merge: {into: "uspopulationyearly", whenMatched: "replace"}}
   ] );
};

# To execute
calculatePopulationCounts();

# Verify
db.uspopulationyearly.find().sort({_id: 1})