import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../generated/app_localizations.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/subcategory_card.dart';
import '../../../core/pages/content_page.dart';

class GamesHubPage extends StatefulWidget {
  final AdService adService;
  const GamesHubPage({super.key, required this.adService});

  @override
  State<GamesHubPage> createState() => _GamesHubPageState();
}

class _GamesHubPageState extends State<GamesHubPage> {
  static const _categories = [
    ContentType.gamingAnecdote,
    ContentType.gamingNomination,
    ContentType.classicGame,
    ContentType.worstGame,
    ContentType.bannedGame,
  ];

  void _navigate(ContentType type) {
    if (type == ContentType.bannedGame) {
      _showBannedWarning();
    } else {
      _doNavigate(type);
    }
  }

  void _showBannedWarning() {
    final loc = AppLocalizations.of(context)!;
    showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text(
          loc.bannedGameWarningTitle,
          style: const TextStyle(color: Colors.white, fontSize: 16),
        ),
        content: Text(
          loc.bannedGameWarningMessage,
          style: const TextStyle(color: Color(0xFFCCCCCC), fontSize: 14, height: 1.5),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(
              loc.goBack,
              style: const TextStyle(color: Colors.grey),
            ),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFB91C1C),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
            onPressed: () {
              Navigator.pop(ctx);
              _doNavigate(ContentType.bannedGame);
            },
            child: Text(loc.continueAnyway),
          ),
        ],
      ),
    );
  }

  void _doNavigate(ContentType type) {
    widget.adService.showInterstitialAd(onComplete: () {
      if (!mounted) return;
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) => ContentPage(contentType: type),
          transitionsBuilder: (_, animation, __, child) =>
              FadeTransition(opacity: animation, child: child),
          transitionDuration: const Duration(milliseconds: 250),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = ContentType.gamesHub.gradient;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(ContentType.gamesHub.icon, size: 24),
            const SizedBox(width: 8),
            Flexible(
              child: Text(
                ContentType.gamesHub.localizedTitle(loc),
                overflow: TextOverflow.ellipsis,
              ),
            ),
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
          child: ListView.builder(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 24),
            itemCount: _categories.length,
            itemBuilder: (context, index) => SubCategoryCard(
              type: _categories[index],
              onNavigate: () => _navigate(_categories[index]),
            ),
          ),
        ),
      ),
    );
  }
}
