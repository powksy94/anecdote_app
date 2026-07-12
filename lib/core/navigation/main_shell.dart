import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../pages/home_page.dart';
import '../../features/favorites/pages/favorites_gate.dart';
import '../../features/onboarding/widgets/onboarding_overlay.dart';
import '../../generated/app_localizations.dart';

class MainShell extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;
  const MainShell({super.key, this.onLocaleChange});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;
  final _generalKey = GlobalKey<NavigatorState>();
  final _favoritesKey = GlobalKey<NavigatorState>();
  bool _showOnboarding = false;

  NavigatorState? get _activeNavigator =>
      _currentIndex == 0 ? _generalKey.currentState : _favoritesKey.currentState;

  @override
  void initState() {
    super.initState();
    _checkOnboarding();
  }

  Future<void> _checkOnboarding() async {
    final prefs = await SharedPreferences.getInstance();
    final done = prefs.getBool('onboarding_done') ?? false;
    if (mounted && !done) setState(() => _showOnboarding = true);
  }

  Future<void> _completeOnboarding() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('onboarding_done', true);
    if (mounted) setState(() => _showOnboarding = false);
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (_activeNavigator?.canPop() == true) _activeNavigator!.pop();
      },
      child: Stack(
        children: [
          Scaffold(
            body: IndexedStack(
              index: _currentIndex,
              children: [
                Navigator(
                  key: _generalKey,
                  pages: [
                    MaterialPage(
                      key: const ValueKey('home'),
                      child: HomePage(onLocaleChange: widget.onLocaleChange),
                    ),
                  ],
                  onDidRemovePage: (_) {},
                ),
                Navigator(
                  key: _favoritesKey,
                  pages: const [
                    MaterialPage(
                      key: ValueKey('favorites'),
                      child: FavoritesGate(),
                    ),
                  ],
                  onDidRemovePage: (_) {},
                ),
              ],
            ),
            bottomNavigationBar: NavigationBar(
              selectedIndex: _currentIndex,
              onDestinationSelected: (i) =>
                  setState(() => _currentIndex = i),
              destinations: [
                NavigationDestination(
                  icon: const Icon(Icons.home_outlined),
                  selectedIcon: const Icon(Icons.home_rounded),
                  label: loc.navGeneral,
                ),
                NavigationDestination(
                  icon: const Icon(Icons.bookmark_outline_rounded),
                  selectedIcon: const Icon(Icons.bookmark_rounded),
                  label: loc.navFavorites,
                ),
              ],
            ),
          ),
          if (_showOnboarding)
            OnboardingOverlay(onDone: _completeOnboarding),
        ],
      ),
    );
  }
}
