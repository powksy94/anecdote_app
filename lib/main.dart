import 'package:flutter/material.dart';
import 'pages/anecdote_page.dart';
import 'pages/language_selection_page.dart';
import 'services/preferences_service.dart';

void main() {
  runApp(const AnecdoteApp());
}

class AnecdoteApp extends StatefulWidget {
  const AnecdoteApp({super.key});

  @override
  State<AnecdoteApp> createState() => _AnecdoteAppState();
}

class _AnecdoteAppState extends State<AnecdoteApp> {
  final prefsService = PreferencesService();
  Locale? _locale;
  bool _showLanguageSelection = false;

  @override
  void initState() {
    super.initState();
    _initApp();
  }

  Future<void> _initApp() async {
    final lang = await prefsService.getLanguagePreference();
    if (lang == 'en' || lang == 'fr') {
      setState(() {
        _locale = Locale(lang);
        _showLanguageSelection = false;
      });
    } else {
      setState(() {
        _showLanguageSelection = true;
      });
    }
  }

  void _onLanguageSelected(Locale locale) {
    setState(() {
      _locale = locale;
      _showLanguageSelection = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.system,
      theme: ThemeData(
        brightness: Brightness.light,
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      locale: _locale,
      supportedLocales: const [
        Locale('en'),
        Locale('fr'),
      ],
      home: _showLanguageSelection
          ? LanguageSelectionPage(onLanguageSelected: _onLanguageSelected)
          : AnecdotePage(onLocaleChange: (locale) {
              setState(() => _locale = locale);
            }),
    );
  }
}
