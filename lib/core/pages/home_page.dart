import 'package:flutter/material.dart';
import './content_page.dart';
import '../../features/world/pages/world_navigator.dart';
import '../../features/space/pages/space_page.dart';
import '../../features/history/pages/history_hub_page.dart';
import '../../features/cinema/pages/cinema_hub_page.dart';
import '../../features/celebrity/pages/celebrity_navigator.dart';
import '../../features/science/pages/science_navigator.dart';
import '../../features/art/pages/art_navigator.dart';
import '../../features/gaming/pages/gaming_navigator.dart';
import '../models/content_type.dart';
import '../services/ad_service.dart';
import '../services/rating_service.dart';
import '../services/version_check_service.dart';
import '../widgets/category_card.dart';
import '../widgets/home_header.dart';
import '../widgets/update_popup_fog.dart';

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
    ContentType.gamingHub,
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
      showUpdateFogDialog(
        context,
        onLater: () => VersionCheckService.snoozeUpdate(),
      );
    } else if (result == VersionCheckResult.justUpdated) {
      showCelebrationDialog(context);
    }

    // Rating : toujours compter l'ouverture, proposer seulement si pas d'update
    final ratingService = RatingService();
    await ratingService.recordOpen();
    if (result == VersionCheckResult.noUpdate && await ratingService.shouldPrompt()) {
      await ratingService.markShown();
      await ratingService.requestReview();
    }
  }

  void _navigate(ContentType type) {
    if (type == ContentType.gamingHub) {
      GamingNavigator.show(context, _adService)
          .then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    if (type == ContentType.scienceHub) {
      ScienceNavigator.show(context, _adService)
          .then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    if (type == ContentType.artHub) {
      ArtNavigator.show(context, _adService)
          .then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    if (type == ContentType.world) {
      WorldNavigator.show(context, _adService)
          .then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    if (type == ContentType.celebrityHub) {
      CelebrityNavigator.show(context, _adService)
          .then((_) => _cardKeys[type]?.currentState?.onNavigationComplete());
      return;
    }
    if (type == ContentType.space ||
        type == ContentType.historyHub || type == ContentType.cinemaHub) {
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) {
            if (type == ContentType.space) return SpacePage(adService: _adService);
            if (type == ContentType.historyHub) return HistoryHubPage(adService: _adService);
            return CinemaHubPage(adService: _adService);
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
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            const HomeHeader(),
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
