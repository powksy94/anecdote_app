import 'package:flutter/material.dart';
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
      if (cached != null &&
          cached.preview.isNotEmpty &&
          cached.preview != 'Content not available') {
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
      if (englishContent == null ||
          englishContent.preview.isEmpty ||
          englishContent.preview == 'Content not available') {
        englishContent = await apiService.fetchContent(widget.contentType);
        await cacheService.saveTodayContent(
          widget.contentType,
          englishContent,
          locale: 'en',
        );
      }

      // 3. Traduire si nécessaire
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
                  ? _buildErrorWidget(theme, gradient)
                  : _buildContentWidget(theme, gradient),
        ),
      ),
    );
  }

  Widget _buildErrorWidget(ThemeData theme, List<Color> gradient) {
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
                  backgroundColor: gradient[0],
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

  Widget _buildContentWidget(ThemeData theme, List<Color> gradient) {
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
                  color: gradient[0].withValues(alpha:0.3),
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
                            gradient[0].withValues(alpha:0.15),
                            gradient[1].withValues(alpha:0.15),
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
                            color: gradient[0],
                          ),
                          const SizedBox(width: 8),
                          Text(
                            showDetails ? loc.hideDetails : loc.showDetails,
                            style: TextStyle(
                              fontSize: 14,
                              color: gradient[0],
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
                              color: gradient[0],
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
                          color: gradient[0].withValues(alpha:0.2),
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
                        color: gradient[0],
                      ),
                      const SizedBox(width: 8),
                      Text(
                        loc.newContentIn(_getTimeUntilMidnight()),
                        style: TextStyle(
                          fontSize: 13,
                          color: gradient[0],
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
