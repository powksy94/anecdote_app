import 'package:flutter/material.dart';
import '../config/env.dart';
import '../../generated/app_localizations.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../services/api_service.dart';
import '../services/content_dispatcher.dart';
import '../services/daily_cache_service.dart';
import '../services/translation_service.dart';
import '../widgets/content_card.dart';
import '../../features/world/widgets/country_card.dart';
import '../../features/cinema/widgets/cinema_card.dart';
import '../widgets/image_content_card.dart';
import '../widgets/error_card.dart';

class ContentPage extends StatefulWidget {
  final ContentType contentType;
  const ContentPage({super.key, required this.contentType});

  @override
  State<ContentPage> createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  late ApiService apiService;
  late DailyCacheService cacheService;
  late TranslationService translationService;
  ContentData? contentData;
  bool isLoading = true;
  bool isFromCache = false;
  bool hasError = false;
  String errorMessage = '';
  String _locale = 'en';

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
  };

  @override
  void initState() {
    super.initState();
    apiService = ApiService(apiKey: Env.apiNinjasKey);
    cacheService = DailyCacheService();
    translationService = TranslationService(apiKey: Env.googleTranslateKey);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final newLocale = Localizations.localeOf(context).languageCode;
    if (newLocale != _locale) {
      _locale = newLocale;
      _loadContent();
    } else if (contentData == null && !isLoading) {
      _loadContent();
    } else if (contentData == null) {
      _loadContent();
    }
  }

  // ── Logique métier ──────────────────────────────────────────────────────

  ContentData _applyLocaleUnits(ContentData content, AppLocalizations l10n) {
    if (_geoTypes.contains(widget.contentType)) {
      var details = content.details;
      details = details.replaceAllMapped(
        RegExp(r'(\d+\.?\d*)B\b'), (m) => '${m[1]}${l10n.popBillion}');
      details = details.replaceAllMapped(
        RegExp(r'(\d+\.?\d*)M\b'), (m) => '${m[1]}${l10n.popMillion}');
      return ContentData(
        preview: content.preview, details: details,
        hasDetails: content.hasDetails, flagSvg: content.flagSvg,
        imageUrl: content.imageUrl, noImageMessage: content.noImageMessage,
        warningText: content.warningText, warningLevel: content.warningLevel);
    }
    if (widget.contentType == ContentType.star) {
      return ContentData(
        preview: content.preview,
        details: content.details.replaceAll(' ly', ' ${l10n.lightYear}'),
        hasDetails: content.hasDetails,
        imageUrl: content.imageUrl,
        noImageMessage: content.noImageMessage);
    }
    if (widget.contentType == ContentType.americanPresident &&
        content.mandateNumber != null) {
      return ContentData(
        preview: '${content.preview} (${_termLabel(content.mandateNumber!, l10n)})',
        details: content.details, hasDetails: content.hasDetails,
        mandateNumber: content.mandateNumber,
        imageUrl: content.imageUrl, noImageMessage: content.noImageMessage);
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

  Future<void> _loadContent() async {
    setState(() { isLoading = true; hasError = false; });
    final l10n = AppLocalizations.of(context)!;
    try {
      final cached = _cinemaTypes.contains(widget.contentType)
          ? null
          : await cacheService.getTodayContent(widget.contentType, locale: _locale);
      final cacheValid = cached != null &&
          cached.preview.isNotEmpty &&
          cached.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet || cached.details.contains('🛸')) &&
          (widget.contentType != ContentType.chuckNorris || cached.preview.length > 20) &&
          (!_imageTypes.contains(widget.contentType) || cached.imageUrl != null || cached.noImageMessage != null);
      if (cacheValid) {
        setState(() { contentData = cached; isLoading = false; isFromCache = true; });
        return;
      }

      ContentData? englishContent = _cinemaTypes.contains(widget.contentType)
          ? null
          : await cacheService.getTodayContent(widget.contentType, locale: 'en');
      final englishCacheValid = englishContent != null &&
          englishContent.preview.isNotEmpty &&
          englishContent.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet || englishContent.details.contains('🛸')) &&
          (widget.contentType != ContentType.chuckNorris || englishContent.preview.length > 20) &&
          (!_cinemaTypes.contains(widget.contentType) || englishContent.quoteLang != null) &&
          (!_imageTypes.contains(widget.contentType) || englishContent.imageUrl != null || englishContent.noImageMessage != null);
      if (!englishCacheValid) {
        englishContent = await fetchDailyContent(widget.contentType, apiService: apiService);
        await cacheService.saveTodayContent(widget.contentType, englishContent, locale: 'en');
      }

      ContentData finalContent = englishContent;
      if (_locale != 'en' && !_cinemaTypes.contains(widget.contentType)) {
        finalContent = await translationService.translateContent(
          _applyLocaleUnits(englishContent, l10n), targetLang: _locale);
        await cacheService.saveTodayContent(widget.contentType, finalContent, locale: _locale);
      }

      setState(() { contentData = finalContent; isLoading = false; isFromCache = false; hasError = false; });
    } catch (e) {
      setState(() { hasError = true; errorMessage = e.toString().replaceAll('Exception: ', ''); isLoading = false; });
    }
  }

  String _getTimeUntilMidnight() {
    final now = DateTime.now();
    final diff = DateTime(now.year, now.month, now.day + 1).difference(now);
    return '${diff.inHours}h ${diff.inMinutes % 60}min';
  }

  // ── Build helpers ───────────────────────────────────────────────────────

  AppBar _buildAppBar(AppLocalizations loc) => AppBar(
        title: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(widget.contentType.icon, size: 24),
          const SizedBox(width: 8),
          Flexible(
            child: Text(widget.contentType.localizedTitle(loc),
                overflow: TextOverflow.ellipsis),
          ),
        ]),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.arrow_back, size: 20),
          ),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          if (!isLoading)
            IconButton(
              icon: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.refresh_rounded, size: 20),
              ),
              onPressed: _loadContent,
            ),
        ],
      );

  Widget _buildContentCard(List<Color> gradient, Color accentColor, String time) {
    if (_cinemaTypes.contains(widget.contentType)) {
      return CinemaCard(contentData: contentData, contentType: widget.contentType,
          gradient: gradient, accentColor: accentColor, timeUntilMidnight: time);
    }
    // Image-based card takes priority over geo card
    if (contentData?.imageUrl != null || contentData?.noImageMessage != null) {
      return ImageContentCard(contentData: contentData, contentType: widget.contentType,
          gradient: gradient, accentColor: accentColor, timeUntilMidnight: time);
    }
    if (_geoTypes.contains(widget.contentType)) {
      return CountryCard(contentData: contentData, gradient: gradient,
          accentColor: accentColor, timeUntilMidnight: time);
    }
    return ContentCard(contentData: contentData, contentType: widget.contentType,
        gradient: gradient, accentColor: accentColor, timeUntilMidnight: time);
  }

  // ── Build ───────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = widget.contentType.gradient;
    final accentColor = widget.contentType.accentColor;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: _buildAppBar(loc),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [gradient[0], gradient[1].withValues(alpha: 0.8), theme.colorScheme.surface],
            stops: const [0.0, 0.3, 0.6],
          ),
        ),
        child: SafeArea(
          child: isLoading
              ? const Center(child: CircularProgressIndicator(color: Colors.white))
              : hasError
                  ? ErrorCard(errorMessage: errorMessage, accentColor: accentColor, onRetry: _loadContent)
                  : _buildContentCard(gradient, accentColor, _getTimeUntilMidnight()),
        ),
      ),
    );
  }
}
