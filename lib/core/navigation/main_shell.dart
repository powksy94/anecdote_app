import 'package:flutter/material.dart';
import '../pages/home_page.dart';
import '../../features/favorites/pages/favorites_gate.dart';
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

  NavigatorState? get _activeNavigator =>
      _currentIndex == 0 ? _generalKey.currentState : _favoritesKey.currentState;

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (_activeNavigator?.canPop() == true) {
          _activeNavigator!.pop();
        }
      },
      child: Scaffold(
        body: IndexedStack(
          index: _currentIndex,
          children: [
            Navigator(
              key: _generalKey,
              onGenerateRoute: (_) => MaterialPageRoute(
                builder: (_) => HomePage(onLocaleChange: widget.onLocaleChange),
              ),
            ),
            Navigator(
              key: _favoritesKey,
              onGenerateRoute: (_) => MaterialPageRoute(
                builder: (_) => const FavoritesGate(),
              ),
            ),
          ],
        ),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: (i) => setState(() => _currentIndex = i),
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
    );
  }
}
