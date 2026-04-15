import 'package:flutter/material.dart';
import '../config/env.dart';
import '../generated/app_localizations.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../services/api_service.dart';
import '../services/daily_cache_service.dart';
import '../services/translation_service.dart';
import '../widgets/content_card.dart';
import '../widgets/country_card.dart';
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

  ContentData _applyLocaleUnits(ContentData content, AppLocalizations l10n) {
    if (widget.contentType != ContentType.country) return content;
    var details = content.details;
    details = details.replaceAllMapped(
      RegExp(r'(\d+\.?\d*)B\b'),
      (m) => '${m[1]}${l10n.popBillion}',
    );
    details = details.replaceAllMapped(
      RegExp(r'(\d+\.?\d*)M\b'),
      (m) => '${m[1]}${l10n.popMillion}',
    );
    return ContentData(
      preview: content.preview,
      details: details,
      hasDetails: content.hasDetails,
      flagSvg: content.flagSvg,
    );
  }

  Future<void> _loadContent() async {
    setState(() {
      isLoading = true;
      hasError = false;
    });

    final l10n = AppLocalizations.of(context)!;

    try {
      final cached = await cacheService.getTodayContent(widget.contentType, locale: _locale);
      final cacheValid = cached != null &&
          cached.preview.isNotEmpty &&
          cached.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet || cached.details.contains('🛸'));
      if (cacheValid) {
        setState(() {
          contentData = cached;
          isLoading = false;
          isFromCache = true;
        });
        return;
      }

      ContentData? englishContent =
          await cacheService.getTodayContent(widget.contentType, locale: 'en');
      final englishCacheValid = englishContent != null &&
          englishContent.preview.isNotEmpty &&
          englishContent.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet || englishContent.details.contains('🛸'));
      if (!englishCacheValid) {
        englishContent = await apiService.fetchContent(widget.contentType);
        await cacheService.saveTodayContent(widget.contentType, englishContent, locale: 'en');
      }

      ContentData finalContent = englishContent;
      if (_locale != 'en') {
        finalContent = await translationService.translateContent(
          _applyLocaleUnits(englishContent, l10n),
          targetLang: _locale,
        );
        await cacheService.saveTodayContent(widget.contentType, finalContent, locale: _locale);
      }

      setState(() {
        contentData = finalContent;
        isLoading = false;
        isFromCache = false;
        hasError = false;
      });
    } catch (e) {
      setState(() {
        hasError = true;
        errorMessage = e.toString().replaceAll('Exception: ', '');
        isLoading = false;
      });
    }
  }

  String _getTimeUntilMidnight() {
    final now = DateTime.now();
    final midnight = DateTime(now.year, now.month, now.day + 1);
    final diff = midnight.difference(now);
    return '${diff.inHours}h ${diff.inMinutes % 60}min';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = widget.contentType.gradient;
    final accentColor = widget.contentType.accentColor;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(widget.contentType.icon, size: 24),
            const SizedBox(width: 8),
            Text(widget.contentType.localizedTitle(loc)),
          ],
        ),
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
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              gradient[0],
              gradient[1].withValues(alpha: 0.8),
              theme.colorScheme.surface,
            ],
            stops: const [0.0, 0.3, 0.6],
          ),
        ),
        child: SafeArea(
          child: isLoading
              ? const Center(child: CircularProgressIndicator(color: Colors.white))
              : hasError
                  ? ErrorCard(
                      errorMessage: errorMessage,
                      accentColor: accentColor,
                      onRetry: _loadContent,
                    )
                  : widget.contentType == ContentType.country
                      ? CountryCard(
                          contentData: contentData,
                          gradient: gradient,
                          accentColor: accentColor,
                          timeUntilMidnight: _getTimeUntilMidnight(),
                        )
                      : ContentCard(
                          contentData: contentData,
                          contentType: widget.contentType,
                          gradient: gradient,
                          accentColor: accentColor,
                          timeUntilMidnight: _getTimeUntilMidnight(),
                        ),
        ),
      ),
    );
  }
}
