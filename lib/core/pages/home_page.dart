import 'package:flutter/material.dart';
import './content_page.dart';
import '../../features/world/pages/world_page.dart';
import '../../features/space/pages/space_page.dart';
import '../../features/history/pages/history_hub_page.dart';
import '../../features/cinema/pages/cinema_hub_page.dart';
import '../../features/celebrity/pages/celebrity_hub_page.dart';
import '../../features/science/pages/science_hub_page.dart';
import '../../features/art/pages/art_hub_page.dart';
import '../models/content_type.dart';
import '../../generated/app_localizations.dart';
import '../services/ad_service.dart';
import '../services/version_check_service.dart';
import '../widgets/category_card.dart';
import '../widgets/update_popup.dart';

class HomePage extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;

  const HomePage({super.key, this.onLocaleChange});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  static const _topLevelTypes = [
    ContentType.anecdote,
    ContentType.cinemaHub,
    ContentType.celebrityHub,
    ContentType.historyHub,
    ContentType.scienceHub,
    ContentType.artHub,
    ContentType.world,
    ContentType.space,
  ];

  final AdService _adService = AdService();
  final Map<ContentType, GlobalKey<_CategoryCardState>> _cardKeys = {
    for (final type in _topLevelTypes) type: GlobalKey(),
  };

  @override
  void initState() {
    super.initState();
    _adService.loadInterstitialAd();
    _checkForUpdate();
  }

  @override
  void dispose() {
    _adService.dispose();
    super.dispose();
  }

  Future<void> _checkForUpdate() async {
    final result = await VersionCheckService().check();
    if (!mounted) return;
    if (result == VersionCheckResult.updateAvailable) {
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const UpdatePopup(mode: UpdatePopupMode.update),
      );
    } else if (result == VersionCheckResult.justUpdated) {
      showDialog(
        context: context,
        barrierDismissible: true,
        builder: (_) => const UpdatePopup(mode: UpdatePopupMode.celebration),
      );
    }
  }

  void _navigate(ContentType type) {
    if (type == ContentType.world || type == ContentType.space ||
        type == ContentType.historyHub || type == ContentType.cinemaHub ||
        type == ContentType.celebrityHub || type == ContentType.scienceHub ||
        type == ContentType.artHub) {
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) {
            if (type == ContentType.world) return WorldPage(adService: _adService);
            if (type == ContentType.space) return SpacePage(adService: _adService);
            if (type == ContentType.historyHub) return HistoryHubPage(adService: _adService);
            if (type == ContentType.cinemaHub) return CinemaHubPage(adService: _adService);
            if (type == ContentType.celebrityHub) return CelebrityHubPage(adService: _adService);
            if (type == ContentType.artHub) return ArtHubPage(adService: _adService);
            return ScienceHubPage(adService: _adService);
          },
          transitionsBuilder: (_, animation, __, child) =>
              FadeTransition(opacity: animation, child: child),
          transitionDuration: const Duration(milliseconds: 250),
        ),
      ).then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    _adService.showInterstitialAd(onComplete: () {
      if (!mounted) return;
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) => ContentPage(contentType: type),
          transitionsBuilder: (_, animation, __, child) =>
              FadeTransition(opacity: animation, child: child),
          transitionDuration: const Duration(milliseconds: 250),
        ),
      ).then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 32),
            Text(
              loc.appTitle,
              style: theme.textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              loc.chooseCategory,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
              ),
            ),
            const SizedBox(height: 32),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: 16,
                    crossAxisSpacing: 16,
                    childAspectRatio: 1.0,
                  ),
                  itemCount: _topLevelTypes.length,
                  itemBuilder: (context, index) {
                    final type = _topLevelTypes[index];
                    return CategoryCard(
                      key: _cardKeys[type],
                      type: type,
                      onNavigate: () => _navigate(type),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

typedef _CategoryCardState = CategoryCardState;
