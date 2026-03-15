import 'package:flutter/material.dart';
import 'pages/home_page.dart';
import 'generated/app_localizations.dart';

class AnecdoteApp extends StatefulWidget {
  const AnecdoteApp({super.key});

  @override
  State<AnecdoteApp> createState() => _AnecdoteAppState();
}

class _AnecdoteAppState extends State<AnecdoteApp> {
  Locale? _locale;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      locale: _locale,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
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
      home: HomePage(
        onLocaleChange: (locale) {
          setState(() => _locale = locale);
        },
      ),
    );
  }
}
