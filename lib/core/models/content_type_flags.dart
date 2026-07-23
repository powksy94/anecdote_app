part of 'content_type.dart';

extension ContentTypeFlags on ContentType {
  static const _geoTypes = {
    ContentType.country,
    ContentType.frenchDepartment,
    ContentType.pacificIsland,
  };

  static const _cinemaTypes = {
    ContentType.classicCinema,
    ContentType.cinema80s90s,
    ContentType.modernCinema,
  };

  // Types dont le contenu doit avoir une image — cache invalidé si imageUrl absent
  static const _imageTypes = {
    ContentType.dinosaur,
    ContentType.battle,
    ContentType.spaceMission,
    ContentType.painting,
    ContentType.frenchCommune,
    ContentType.americanState,
    ContentType.kingOfFrance,
    ContentType.americanPresident,
    ContentType.solarSystemMoon,
    ContentType.frenchDepartment,
    ContentType.animals,
    ContentType.sculpture,
    ContentType.architecture,
    ContentType.famousArtist,
    ContentType.photographer,
    ContentType.classicalComposer,
    ContentType.nobelPrize,
    ContentType.chemicalElement,
    ContentType.volcano,
    ContentType.insect,
    ContentType.bird,
    ContentType.mineral,
    ContentType.cloud,
    ContentType.humanBone,
    ContentType.exoplanet,
    ContentType.star,
    ContentType.lgbtqiaPersonality,
    ContentType.pioneerWoman,
    ContentType.legendaryAthlete,
    ContentType.gamingLegend,
    ContentType.classicGame,
    ContentType.gamingNomination,
    ContentType.worstGame,
    ContentType.bannedGame,
    ContentType.musicLegend,
    ContentType.album,
    ContentType.instrument,
    ContentType.musicFestival,
    ContentType.musicAward,
    ContentType.greekMythology,
    ContentType.norseMythology,
    ContentType.egyptianMythology,
    ContentType.mythologicalCreature,
  };

  // Game/person names in preview should NOT be translated
  static const _untranslatablePreviewTypes = {
    ContentType.classicGame,
    ContentType.worstGame,
    ContentType.bannedGame,
    ContentType.gamingNomination,
    ContentType.gamingLegend,
    ContentType.musicLegend,
    ContentType.album,
    ContentType.musicFestival,
    ContentType.musicAward,
    ContentType.greekMythology,
    ContentType.norseMythology,
    ContentType.egyptianMythology,
    ContentType.mythologicalCreature,
  };

  bool get isGeoType => _geoTypes.contains(this);
  bool get isCinemaType => _cinemaTypes.contains(this);
  bool get requiresImage => _imageTypes.contains(this);
  bool get hasUntranslatablePreview => _untranslatablePreviewTypes.contains(this);
}
