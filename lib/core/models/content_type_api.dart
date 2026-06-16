part of 'content_type.dart';

extension ContentTypeApi on ContentType {
  String get apiEndpoint {
    switch (this) {
      case ContentType.anecdote:
        return 'https://api.api-ninjas.com/v1/facts';
      case ContentType.chuckNorris:
        return 'https://api.api-ninjas.com/v1/chucknorris';
      case ContentType.celebrityQuote:
        return 'https://api.api-ninjas.com/v1/quotes?category=inspirational';
      case ContentType.history:
        return 'https://api.api-ninjas.com/v1/historicalevents';
      case ContentType.animals:
        return 'https://api.api-ninjas.com/v1/animals?name=lion';
      case ContentType.country:
      case ContentType.frenchDepartment:
      case ContentType.pacificIsland:
      case ContentType.world:
      case ContentType.exoplanet:
      case ContentType.star:
      case ContentType.solarSystemMoon:
      case ContentType.space:
      case ContentType.kingOfFrance:
      case ContentType.americanPresident:
      case ContentType.historyHub:
      case ContentType.cinemaHub:
      case ContentType.classicCinema:
      case ContentType.cinema80s90s:
      case ContentType.modernCinema:
      case ContentType.celebrityHub:
      case ContentType.scienceHub:
      case ContentType.dinosaur:
      case ContentType.spaceMission:
      case ContentType.battle:
      case ContentType.artHub:
      case ContentType.painting:
      case ContentType.sculpture:
      case ContentType.architecture:
      case ContentType.famousArtist:
      case ContentType.photographer:
      case ContentType.classicalComposer:
      case ContentType.nobelPrize:
      case ContentType.frenchCommune:
      case ContentType.americanState:
      case ContentType.scienceLivingHub:
      case ContentType.scienceNonLivingHub:
      case ContentType.artWorksHub:
      case ContentType.artArtistsHub:
      case ContentType.chemicalElement:
      case ContentType.volcano:
      case ContentType.insect:
      case ContentType.bird:
      case ContentType.mineral:
      case ContentType.cloud:
      case ContentType.humanBone:
      case ContentType.territoriesHub:
      case ContentType.naturalWondersHub:
        return '';
    }
  }
}
