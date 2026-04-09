import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../config/env.dart';
import '../generated/app_localizations.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../services/api_service.dart';
import '../services/daily_cache_service.dart';
import '../services/translation_service.dart';

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
  bool showDetails = false;
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

  Future<void> _loadContent() async {
    setState(() {
      isLoading = true;
      hasError = false;
    });

    try {
      // 1. Vérifier le cache pour la locale courante
      final cached = await cacheService.getTodayContent(
        widget.contentType,
        locale: _locale,
      );
      // Pour exoplanet, ignorer le cache s'il ne contient pas les emojis de détail (version antérieure)
      final cacheValid = cached != null &&
          cached.preview.isNotEmpty &&
          cached.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet ||
              cached.details.contains('🛸'));
      if (cacheValid) {
        setState(() {
          contentData = cached;
          isLoading = false;
          isFromCache = true;
        });
        return;
      }

      // 2. Récupérer le contenu anglais (cache ou API)
      ContentData? englishContent = await cacheService.getTodayContent(
        widget.contentType,
        locale: 'en',
      );
      // Même vérification d'intégrité que pour la locale courante
      final englishCacheValid = englishContent != null &&
          englishContent.preview.isNotEmpty &&
          englishContent.preview != 'Content not available' &&
          (widget.contentType != ContentType.exoplanet ||
              englishContent.details.contains('🛸'));
      if (!englishCacheValid) {
        englishContent = await apiService.fetchContent(widget.contentType);
        await cacheService.saveTodayContent(
          widget.contentType,
          englishContent,
          locale: 'en',
        );
      }

      // 3. Traduire si nécessaire (emojis préservés via placeholders dans TranslationService)
      ContentData finalContent = englishContent;
      if (_locale != 'en') {
        finalContent = await translationService.translateContent(
          englishContent,
          targetLang: _locale,
        );
        await cacheService.saveTodayContent(
          widget.contentType,
          finalContent,
          locale: _locale,
        );
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
    final hours = diff.inHours;
    final minutes = diff.inMinutes % 60;
    return '${hours}h ${minutes}min';
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
              color: Colors.white.withValues(alpha:0.2),
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
                  color: Colors.white.withValues(alpha:0.2),
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
              gradient[1].withValues(alpha:0.8),
              theme.colorScheme.surface,
            ],
            stops: const [0.0, 0.3, 0.6],
          ),
        ),
        child: SafeArea(
          child: isLoading
              ? const Center(
                  child: CircularProgressIndicator(color: Colors.white),
                )
              : hasError
                  ? _buildErrorWidget(theme, gradient, accentColor)
                  : _buildContentWidget(theme, gradient, accentColor),
        ),
      ),
    );
  }

  Widget _buildCountryContent(ThemeData theme, List<Color> gradient, Color accentColor) {
    final loc = AppLocalizations.of(context)!;
    final preview = contentData?.preview ?? '';
    final emojiFlag = RegExp(r'[\u{1F1E0}-\u{1F1FF}]{2}', unicode: true).firstMatch(preview)?.group(0) ?? '🌍';
    final countryName = preview.replaceAll(RegExp(r'[\u{1F1E0}-\u{1F1FF}]{2}\s*', unicode: true), '').trim();
    final detailLines = (contentData?.details ?? '')
        .split('\n')
        .where((l) => l.trim().isNotEmpty)
        .toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: accentColor.withValues(alpha:0.3),
                  blurRadius: 30,
                  spreadRadius: 5,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Flag SVG — full width, top of card
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                  child: contentData?.flagSvg != null
                      ? SvgPicture.string(
                          contentData!.flagSvg!,
                          width: double.infinity,
                          fit: BoxFit.fitWidth,
                        )
                      : Container(
                          height: 160,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(colors: gradient),
                          ),
                          child: Center(
                            child: Text(emojiFlag, style: const TextStyle(fontSize: 100)),
                          ),
                        ),
                ),
                // Country name
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 20, 24, 4),
                  child: Text(
                    countryName,
                    textAlign: TextAlign.center,
                    style: theme.textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: Divider(color: accentColor.withValues(alpha:0.3)),
                ),
                // Detail rows — always visible
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 8, 24, 20),
                  child: Column(
                    children: detailLines.map((line) {
                      final parts = line.split(':');
                      final label = parts[0].trim();
                      final value = parts.length > 1 ? parts.sublist(1).join(':').trim() : '';
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(label, style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w600)),
                            if (value.isNotEmpty) ...[
                              const SizedBox(width: 4),
                              const Text(':'),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  value,
                                  style: theme.textTheme.bodyMedium?.copyWith(
                                    color: theme.colorScheme.onSurface.withValues(alpha: 0.75),
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ),
                // Timer badge
                Padding(
                  padding: const EdgeInsets.only(bottom: 20),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.schedule_rounded, size: 16, color: accentColor),
                          const SizedBox(width: 8),
                          Text(
                            loc.newContentIn(_getTimeUntilMidnight()),
                            style: TextStyle(fontSize: 13, color: accentColor, fontWeight: FontWeight.w500),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorWidget(ThemeData theme, List<Color> gradient, Color accentColor) {
    final loc = AppLocalizations.of(context)!;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Container(
          constraints: const BoxConstraints(maxWidth: 400),
          padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(
            color: theme.colorScheme.surface,
            borderRadius: BorderRadius.circular(24),
            boxShadow: [
              BoxShadow(
                color: Colors.red.withValues(alpha:0.2),
                blurRadius: 30,
                spreadRadius: 5,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.withValues(alpha:0.1),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Icon(
                  Icons.cloud_off_rounded,
                  size: 48,
                  color: Colors.red,
                ),
              ),
              const SizedBox(height: 24),
              Text(
                loc.unableToLoad,
                textAlign: TextAlign.center,
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                errorMessage,
                textAlign: TextAlign.center,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: theme.colorScheme.onSurface.withValues(alpha:0.6),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _loadContent,
                icon: const Icon(Icons.refresh_rounded),
                label: Text(loc.retry),
                style: ElevatedButton.styleFrom(
                  backgroundColor: accentColor,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 32,
                    vertical: 16,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildContentWidget(ThemeData theme, List<Color> gradient, Color accentColor) {
    if (widget.contentType == ContentType.country) {
      return _buildCountryContent(theme, gradient, accentColor);
    }
    final loc = AppLocalizations.of(context)!;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: accentColor.withValues(alpha:0.3),
                  blurRadius: 30,
                  spreadRadius: 5,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: gradient),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(
                    widget.contentType.icon,
                    size: 40,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 24),
                Text(
                  contentData?.preview ?? '',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontSize: 20,
                    height: 1.5,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                if (contentData?.hasDetails == true) ...[
                  const SizedBox(height: 20),
                  GestureDetector(
                    onTap: () => setState(() => showDetails = !showDetails),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 12,
                      ),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            accentColor.withValues(alpha:0.15),
                            accentColor.withValues(alpha:0.08),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            showDetails
                                ? Icons.visibility_off_rounded
                                : Icons.visibility_rounded,
                            size: 20,
                            color: accentColor,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            showDetails ? loc.hideDetails : loc.showDetails,
                            style: TextStyle(
                              fontSize: 14,
                              color: accentColor,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(width: 4),
                          AnimatedRotation(
                            turns: showDetails ? 0.5 : 0,
                            duration: const Duration(milliseconds: 200),
                            child: Icon(
                              Icons.keyboard_arrow_down_rounded,
                              size: 20,
                              color: accentColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  AnimatedCrossFade(
                    firstChild: const SizedBox.shrink(),
                    secondChild: Container(
                      width: double.infinity,
                      margin: const EdgeInsets.only(top: 16),
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha:0.5),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: accentColor.withValues(alpha:0.2),
                          width: 1,
                        ),
                      ),
                      child: Text(
                        contentData?.details ?? '',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          height: 1.6,
                        ),
                      ),
                    ),
                    crossFadeState: showDetails
                        ? CrossFadeState.showSecond
                        : CrossFadeState.showFirst,
                    duration: const Duration(milliseconds: 300),
                  ),
                ],
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.surfaceContainerHighest.withValues(alpha:0.5),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.schedule_rounded,
                        size: 16,
                        color: accentColor,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        loc.newContentIn(_getTimeUntilMidnight()),
                        style: TextStyle(
                          fontSize: 13,
                          color: accentColor,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
