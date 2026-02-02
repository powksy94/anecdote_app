import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'pages/anecdote_page.dart';
import 'services/preferences_service.dart';
import 'generated/app_localizations.dart';

class AnecdoteApp extends StatefulWidget {
  const AnecdoteApp({super.key});

  @override
  State<AnecdoteApp> createState() => _AnecdoteAppState();
}

class _AnecdoteAppState extends State<AnecdoteApp> {
  final prefsService = PreferencesService();
  Locale? _locale;

  @override
  void initState() {
    super.initState();
    _loadLocale();
  }

  Future<void> _loadLocale() async {
    final lang = await prefsService.getLanguagePreference();
    setState(() {
      _locale = Locale(lang);
    });
  }

  void _changeLocale(Locale locale) async {
    setState(() => _locale = locale);
    await prefsService.saveLanguagePreference(locale.languageCode);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      onGenerateTitle: (context) => AppLocalizations.of(context)!.appTitle,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      locale: _locale,
      supportedLocales: const [
        Locale('en'),
        Locale('fr'),
      ],
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      home: AnecdotePage(
        onLocaleChange: _changeLocale, // Passe le callback à la page
      ),
    );
  }
}
