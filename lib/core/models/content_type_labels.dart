part of 'content_type.dart';

extension ContentTypeLabels on ContentType {
  String get title {
    switch (this) {
      case ContentType.anecdote:           return 'Anecdote';
      case ContentType.chuckNorris:        return 'Chuck Norris';
      case ContentType.celebrityQuote:     return 'Celebrity Quote';
      case ContentType.history:            return 'Day of History';
      case ContentType.kingOfFrance:       return 'Kings of France';
      case ContentType.americanPresident:  return 'American Presidents';
      case ContentType.historyHub:         return 'History';
      case ContentType.animals:            return 'Animals';
      case ContentType.frenchDepartment:   return 'French Department';
      case ContentType.pacificIsland:      return 'Pacific Island';
      case ContentType.country:            return 'Countries';
      case ContentType.world:              return 'World';
      case ContentType.exoplanet:          return 'Exoplanet';
      case ContentType.star:               return 'Star';
      case ContentType.solarSystemMoon:    return 'Moon';
      case ContentType.space:              return 'Space';
      case ContentType.cinemaHub:          return 'Cinema';
      case ContentType.classicCinema:      return 'Classic Hollywood';
      case ContentType.cinema80s90s:       return '80s & 90s Movies';
      case ContentType.modernCinema:       return 'Modern Cinema';
      case ContentType.celebrityHub:       return 'Celebrity';
      case ContentType.scienceHub:         return 'Science & Nature';
      case ContentType.dinosaur:           return 'Dinosaurs';
      case ContentType.spaceMission:       return 'Space Missions';
      case ContentType.battle:             return 'Historical Battles';
      case ContentType.artHub:             return 'Art & Culture';
      case ContentType.painting:           return 'Famous Paintings';
      case ContentType.sculpture:          return 'Famous Sculptures';
      case ContentType.architecture:       return 'Iconic Architecture';
      case ContentType.famousArtist:       return 'Famous Artists';
      case ContentType.photographer:       return 'Photographers';
      case ContentType.classicalComposer:  return 'Classical Composers';
      case ContentType.nobelPrize:         return 'Nobel Prize';
      case ContentType.frenchCommune:      return 'French Communes';
      case ContentType.americanState:      return 'American States';
    }
  }

  String localizedTitle(AppLocalizations loc) {
    switch (this) {
      case ContentType.anecdote:           return loc.categoryAnecdote;
      case ContentType.chuckNorris:        return loc.categoryChuckNorris;
      case ContentType.celebrityQuote:     return loc.categoryAdvice;
      case ContentType.history:            return loc.categoryDayOfHistory;
      case ContentType.kingOfFrance:       return loc.categoryKingOfFrance;
      case ContentType.americanPresident:  return loc.categoryAmericanPresident;
      case ContentType.historyHub:         return loc.categoryHistoryHub;
      case ContentType.animals:            return loc.categoryAnimals;
      case ContentType.country:            return loc.categoryCountry;
      case ContentType.frenchDepartment:   return loc.categoryFrenchDepartment;
      case ContentType.pacificIsland:      return loc.categoryPacificIsland;
      case ContentType.world:              return loc.categoryWorld;
      case ContentType.exoplanet:          return loc.categoryExoplanet;
      case ContentType.star:               return loc.categoryStar;
      case ContentType.solarSystemMoon:    return loc.categorySolarSystemMoon;
      case ContentType.space:              return loc.categorySpace;
      case ContentType.cinemaHub:          return loc.categoryCinemaHub;
      case ContentType.classicCinema:      return loc.categoryClassicCinema;
      case ContentType.cinema80s90s:       return loc.categoryCinema80s90s;
      case ContentType.modernCinema:       return loc.categoryModernCinema;
      case ContentType.celebrityHub:       return loc.categoryCelebrityHub;
      case ContentType.scienceHub:         return loc.categoryScienceHub;
      case ContentType.dinosaur:           return loc.categoryDinosaur;
      case ContentType.spaceMission:       return loc.categorySpaceMission;
      case ContentType.battle:             return loc.categoryBattle;
      case ContentType.artHub:             return loc.categoryArtHub;
      case ContentType.painting:           return loc.categoryPainting;
      case ContentType.sculpture:          return loc.categorySculpture;
      case ContentType.architecture:       return loc.categoryArchitecture;
      case ContentType.famousArtist:       return loc.categoryFamousArtist;
      case ContentType.photographer:       return loc.categoryPhotographer;
      case ContentType.classicalComposer:  return loc.categoryClassicalComposer;
      case ContentType.nobelPrize:         return loc.categoryNobelPrize;
      case ContentType.frenchCommune:      return loc.categoryFrenchCommune;
      case ContentType.americanState:      return loc.categoryAmericanState;
    }
  }
}
