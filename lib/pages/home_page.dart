import 'package:flutter/material.dart';
import 'content_page.dart';
import '../models/content_type.dart';
import '../generated/app_localizations.dart';
import '../services/ad_service.dart';
import '../widgets/category_card.dart';

class HomePage extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;

  const HomePage({super.key, this.onLocaleChange});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final AdService _adService = AdService();
  final Map<ContentType, GlobalKey<_CategoryCardState>> _cardKeys = {
    for (final type in ContentType.values) type: GlobalKey(),
  };

  @override
  void initState() {
    super.initState();
    _adService.loadInterstitialAd();
  }

  @override
  void dispose() {
    _adService.dispose();
    super.dispose();
  }

  void _navigate(ContentType type) {
    _adService.showInterstitialAd(onComplete: () {
      if (!mounted) return;
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (context, animation, secondaryAnimation) =>
              ContentPage(contentType: type),
          transitionsBuilder: (context, animation, secondaryAnimation, child) =>
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
                  itemCount: ContentType.values.length,
                  itemBuilder: (context, index) {
                    final type = ContentType.values[index];
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

// Alias pour accès au state depuis HomePage via GlobalKey
typedef _CategoryCardState = CategoryCardState;
