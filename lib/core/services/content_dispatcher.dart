import '../models/content_type.dart';
import '../models/content_data.dart';
import 'api_service.dart';
import '../../features/world/services/country_service.dart';
import '../../features/world/services/department_service.dart';
import '../../features/world/services/pacific_island_service.dart';
import '../../features/world/services/commune_service.dart';
import '../../features/world/services/state_service.dart';
import '../../features/world/services/volcano_service.dart';
import '../../features/space/services/star_service.dart';
import '../../features/space/services/moon_service.dart';
import '../../features/space/services/mission_service.dart';
import '../../features/space/services/exoplanet_service.dart';
import '../../features/history/services/king_service.dart';
import '../../features/history/services/president_service.dart';
import '../../features/history/services/battle_service.dart';
import '../../features/cinema/services/cinema_service.dart';
import '../../features/science/services/dinosaur_service.dart';
import '../../features/science/services/chemical_element_service.dart';
import '../../features/science/services/insect_service.dart';
import '../../features/science/services/bird_service.dart';
import '../../features/science/services/mineral_service.dart';
import '../../features/science/services/cloud_service.dart';
import '../../features/science/services/human_bone_service.dart';
import '../../features/art/services/painting_service.dart';
import '../../features/art/services/sculpture_service.dart';
import '../../features/art/services/architecture_service.dart';
import '../../features/art/services/famous_artist_service.dart';
import '../../features/art/services/photographer_service.dart';
import '../../features/art/services/classical_composer_service.dart';
import '../../features/art/services/nobel_prize_service.dart';

Future<ContentData> fetchDailyContent(
  ContentType type, {
  required ApiService apiService,
}) async {
  switch (type) {
    // ── World ──────────────────────────────────────────────────────────────
    case ContentType.country:          return CountryService().getDailyContent();
    case ContentType.frenchDepartment: return DepartmentService().getDailyContent();
    case ContentType.pacificIsland:    return PacificIslandsService().getDailyContent();
    case ContentType.frenchCommune:    return CommuneService().getDailyContent();
    case ContentType.americanState:    return StateService().getDailyContent();
    case ContentType.volcano:          return VolcanoService().getDailyContent();
    // ── Space ──────────────────────────────────────────────────────────────
    case ContentType.exoplanet:        return ExoplanetService().getDailyContent();
    case ContentType.star:             return StarService().getDailyContent();
    case ContentType.solarSystemMoon:  return MoonService().getDailyContent();
    case ContentType.spaceMission:     return SpaceMissionService().getDailyContent();
    // ── History ────────────────────────────────────────────────────────────
    case ContentType.kingOfFrance:       return KingService().getDailyContent();
    case ContentType.americanPresident:  return PresidentService().getDailyContent();
    case ContentType.battle:             return BattleService().getDailyContent();
    // ── Cinema ─────────────────────────────────────────────────────────────
    case ContentType.classicCinema:
    case ContentType.cinema80s90s:
    case ContentType.modernCinema:     return CinemaService(type).getDailyContent();
    // ── Science (living) ───────────────────────────────────────────────────
    case ContentType.dinosaur:         return DinosaurService().getDailyContent();
    case ContentType.insect:           return InsectService().getDailyContent();
    case ContentType.bird:             return BirdService().getDailyContent();
    // ── Science (non-living) ───────────────────────────────────────────────
    case ContentType.chemicalElement:  return ChemicalElementService().getDailyContent();
    case ContentType.mineral:          return MineralService().getDailyContent();
    case ContentType.cloud:            return CloudService().getDailyContent();
    case ContentType.humanBone:        return HumanBoneService().getDailyContent();
    // ── Art ────────────────────────────────────────────────────────────────
    case ContentType.painting:         return PaintingService().getDailyContent();
    case ContentType.sculpture:        return SculptureService().getDailyContent();
    case ContentType.architecture:     return ArchitectureService().getDailyContent();
    case ContentType.famousArtist:     return FamousArtistService().getDailyContent();
    case ContentType.photographer:     return PhotographerService().getDailyContent();
    case ContentType.classicalComposer:return ClassicalComposerService().getDailyContent();
    case ContentType.nobelPrize:       return NobelPrizeService().getDailyContent();
    // ── API-ninjas / HTTP ──────────────────────────────────────────────────
    default:                           return apiService.fetchRemoteContent(type);
  }
}
