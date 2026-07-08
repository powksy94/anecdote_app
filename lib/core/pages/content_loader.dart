import '../../generated/app_localizations.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../services/api_service.dart';
import '../services/content_dispatcher.dart';
import '../services/daily_cache_service.dart';
import '../services/translation_service.dart';

/// Charge le contenu du jour pour un [ContentType] : relit le cache local,
/// retombe sur un appel réseau + traduction si absent ou invalide, et
/// sauvegarde le résultat. Ne touche à aucun état de widget — l'appelant
/// gère le setState autour de [load].
class ContentLoader {
  final ContentType contentType;
  final ApiService apiService;
  final DailyCacheService cacheService;
  final TranslationService translationService;

  ContentLoader({
    required this.contentType,
    required this.apiService,
    required this.cacheService,
    required this.translationService,
  });

  ContentData _applyLocaleUnits(ContentData content, AppLocalizations l10n) {
    if (contentType.isGeoType) {
      var details = content.details;
      details = details.replaceAllMapped(
        RegExp(r'(\d+\.?\d*)B\b'), (m) => '${m[1]}${l10n.popBillion}');
      details = details.replaceAllMapped(
        RegExp(r'(\d+\.?\d*)M\b'), (m) => '${m[1]}${l10n.popMillion}');
      return ContentData(
        preview: content.preview, details: details,
        hasDetails: content.hasDetails, flagSvg: content.flagSvg,
        imageUrl: content.imageUrl, noImageMessage: content.noImageMessage,
        warningText: content.warningText, warningLevel: content.warningLevel,
        imageNote: content.imageNote);
    }
    if (contentType == ContentType.star) {
      return ContentData(
        preview: content.preview,
        details: content.details.replaceAll(' ly', ' ${l10n.lightYear}'),
        hasDetails: content.hasDetails,
        imageUrl: content.imageUrl,
        noImageMessage: content.noImageMessage,
        imageNote: content.imageNote);
    }
    if (contentType == ContentType.americanPresident &&
        content.mandateNumber != null) {
      return ContentData(
        preview: '${content.preview} (${_termLabel(content.mandateNumber!, l10n)})',
        details: content.details, hasDetails: content.hasDetails,
        mandateNumber: content.mandateNumber,
        imageUrl: content.imageUrl, noImageMessage: content.noImageMessage,
        imageNote: content.imageNote);
    }
    return content;
  }

  String _termLabel(int n, AppLocalizations l10n) {
    switch (n) {
      case 1: return l10n.term1;
      case 2: return l10n.term2;
      case 3: return l10n.term3;
      case 4: return l10n.term4;
      default: return '$n';
    }
  }

  bool _isUsable(ContentData? data) {
    if (data == null) return false;
    if (data.preview.isEmpty || data.preview == 'Content not available') return false;
    if (contentType == ContentType.exoplanet && !data.details.contains('🛸')) return false;
    if (contentType == ContentType.chuckNorris && data.preview.length <= 20) return false;
    if (contentType.requiresImage && data.imageUrl == null && data.noImageMessage == null) return false;
    return true;
  }

  /// Retourne le contenu du jour dans [locale]. Si [forceRefresh] est vrai,
  /// ignore tout cache existant et réécrit la valeur sauvegardée.
  Future<ContentData> load({
    required AppLocalizations l10n,
    required String locale,
    bool forceRefresh = false,
  }) async {
    final cached = forceRefresh || contentType.isCinemaType
        ? null
        : await cacheService.getTodayContent(contentType, locale: locale);
    if (_isUsable(cached)) return cached!;

    ContentData? englishContent = forceRefresh || contentType.isCinemaType
        ? null
        : await cacheService.getTodayContent(contentType, locale: 'en');
    final englishCacheValid = _isUsable(englishContent) &&
        (!contentType.isCinemaType || englishContent!.quoteLang != null);
    if (!englishCacheValid) {
      englishContent = await fetchDailyContent(contentType, apiService: apiService);
      await cacheService.saveTodayContent(contentType, englishContent, locale: 'en');
    }

    if (locale == 'en' || contentType.isCinemaType) {
      return englishContent!;
    }

    final finalContent = await translationService.translateContent(
      _applyLocaleUnits(englishContent!, l10n),
      targetLang: locale,
      skipPreview: contentType.hasUntranslatablePreview,
    );
    await cacheService.saveTodayContent(contentType, finalContent, locale: locale);
    return finalContent;
  }
}
