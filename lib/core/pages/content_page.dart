import 'package:flutter/material.dart';
import '../config/env.dart';
import '../../features/auth/pages/login_page.dart';
import '../../features/favorites/controllers/favorite_toggle_controller.dart';
import '../../generated/app_localizations.dart';
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../services/api_service.dart';
import '../services/daily_cache_service.dart';
import '../services/translation_service.dart';
import '../widgets/layout/content_app_bar.dart';
import '../widgets/cards/content_card_selector.dart';
import '../widgets/layout/error_card.dart';
import './content_loader.dart';

class ContentPage extends StatefulWidget {
  final ContentType contentType;
  const ContentPage({super.key, required this.contentType});

  @override
  State<ContentPage> createState() => _ContentPageState();
}

class _ContentPageState extends State<ContentPage> {
  late ContentLoader _loader;
  final _favoriteCtrl = FavoriteToggleController();
  ContentData? contentData;
  bool isLoading = true;
  bool hasError = false;
  String errorMessage = '';
  String _locale = 'en';
  bool _isFavorited = false;

  @override
  void initState() {
    super.initState();
    _loader = ContentLoader(
      contentType: widget.contentType,
      apiService: ApiService(apiKey: Env.apiNinjasKey),
      cacheService: DailyCacheService(),
      translationService: TranslationService(apiKey: Env.googleTranslateKey),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final newLocale = Localizations.localeOf(context).languageCode;
    if (newLocale != _locale) {
      _locale = newLocale;
      _loadContent();
    } else if (contentData == null) {
      _loadContent();
    }
  }

  Future<void> _loadContent({bool forceRefresh = false}) async {
    setState(() { isLoading = true; hasError = false; });
    final l10n = AppLocalizations.of(context)!;
    try {
      final result = await _loader.load(
        l10n: l10n, locale: _locale, forceRefresh: forceRefresh);
      final favorited = await _favoriteCtrl.isFavorite(
          widget.contentType, result.preview);
      if (!mounted) return;
      setState(() {
        contentData = result;
        _isFavorited = favorited;
        isLoading = false;
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

  Future<void> _toggleFavorite() async {
    if (contentData == null) return;
    final newState = await _favoriteCtrl.toggle(
        widget.contentType, contentData!.preview,
        details: contentData!.hasDetails ? contentData!.details : '');
    if (!mounted) return;
    if (newState == null) {
      Navigator.push(
          context, MaterialPageRoute(builder: (_) => const LoginPage()));
    } else {
      setState(() => _isFavorited = newState);
    }
  }

  String _getTimeUntilMidnight() {
    final now = DateTime.now();
    final diff = DateTime(now.year, now.month, now.day + 1).difference(now);
    return '${diff.inHours}h ${diff.inMinutes % 60}min';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final gradient = widget.contentType.gradient;
    final accentColor = widget.contentType.accentColor;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: ContentAppBar(
        contentType: widget.contentType,
        isLoading: isLoading,
        onBack: () => Navigator.pop(context),
        onRefresh: () => _loadContent(forceRefresh: true),
        isFavorited: _isFavorited,
        onFavorite: contentData != null ? _toggleFavorite : null,
      ),
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
                  ? ErrorCard(errorMessage: errorMessage, accentColor: accentColor, onRetry: () => _loadContent(forceRefresh: true))
                  : selectContentCard(
                      contentType: widget.contentType,
                      contentData: contentData,
                      gradient: gradient,
                      accentColor: accentColor,
                      timeUntilMidnight: _getTimeUntilMidnight(),
                    ),
        ),
      ),
    );
  }
}
