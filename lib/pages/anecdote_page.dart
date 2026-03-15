import 'dart:async';
import 'package:flutter/material.dart';
import '../config/env.dart';
import '../services/fact_service.dart';
import '../services/preferences_service.dart';
import '../services/daily_fact_service.dart';
import '../widgets/anecdote_card.dart';
import '../models/fact.dart';
import '../generated/app_localizations.dart';

class AnecdotePage extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;

  const AnecdotePage({super.key, this.onLocaleChange});

  @override
  State<AnecdotePage> createState() => _AnecdotePageState();
}

class _AnecdotePageState extends State<AnecdotePage> {
  late FactService factService;
  late PreferencesService prefsService;
  late DailyFactCache dailyCache;
  Timer? _midnightTimer;

  Fact? fact;
  bool isLoading = true;
  bool showAnecdote = false;
  bool showDetails = false;
  String displayedText = '';
  String? language;

  @override
  void initState() {
    super.initState();
    factService = FactService(apiKey: Env.apiNinjasKey);
    prefsService = PreferencesService();
    dailyCache = DailyFactCache();

    _loadLanguagePreference();
    _loadDailyFact();
    _scheduleMidnightReset();
  }

  @override
  void dispose() {
    _midnightTimer?.cancel();
    super.dispose();
  }

  void _scheduleMidnightReset() {
    final now = DateTime.now();
    final tomorrow = DateTime(now.year, now.month, now.day + 1);
    final duration = tomorrow.difference(now);

    _midnightTimer = Timer(duration, () async {
      await dailyCache.clearCache();
      _loadDailyFact();
      _scheduleMidnightReset();
    });
  }

  Future<void> _loadLanguagePreference() async {
    final lang = await prefsService.getLanguagePreference();
    setState(() => language = lang ?? 'en'); // fallback en anglais
    widget.onLocaleChange?.call(Locale(language!));
  }

  Future<void> _loadDailyFact() async {
    setState(() => isLoading = true);

    try {
      final cached = await dailyCache.getTodayFact();
      String text;

      if (cached != null) {
        text = cached['original'];
      } else {
        final fetchedFact = await factService.fetchFactOfTheDay();
        text = fetchedFact.text;
        await dailyCache.saveTodayFact(original: text);
      }

      setState(() {
        displayedText = text;
        fact = Fact(text: text);
        showAnecdote = true;
        isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      final loc = AppLocalizations.of(context)!;
      setState(() {
        displayedText = '${loc.error}: $e';
        showAnecdote = true;
        isLoading = false;
      });
    }
  }

  Future<void> changeLanguage(String lang) async {
    setState(() => isLoading = true);
    await prefsService.saveLanguagePreference(lang);

    setState(() {
      language = lang;
      isLoading = false;
    });

    widget.onLocaleChange?.call(Locale(lang));
    _loadDailyFact(); // recharge le texte traduit
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Scaffold(
      backgroundColor: theme.colorScheme.surface,
      appBar: AppBar(
        title: Text(loc.appTitle),
        centerTitle: true,
        backgroundColor: theme.colorScheme.primary,
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language),
            onSelected: changeLanguage,
            itemBuilder: (context) => [
              PopupMenuItem(value: 'en', child: Text('English')),
              PopupMenuItem(value: 'fr', child: Text('Français')),
            ],
          ),
        ],
      ),
      body: Center(
        child: isLoading
            ? const CircularProgressIndicator()
            : AnimatedOpacity(
                opacity: showAnecdote ? 1.0 : 0.0,
                duration: const Duration(milliseconds: 600),
                curve: Curves.easeIn,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    AnecdoteCard(
                      text: displayedText,
                      showDetails: showDetails,
                      onTap: () => setState(() => showDetails = !showDetails),
                    ),
                  ],
                ),
              ),
      ),
    );
  }
}
