import 'dart:async';
import 'package:flutter/material.dart';
import '../services/fact_service.dart';
import '../services/translate_service.dart';
import '../services/preferences_service.dart';
import '../services/daily_fact_service.dart';
import '../widgets/anecdote_card.dart';
import '../models/fact.dart';

class AnecdotePage extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;

  const AnecdotePage({super.key, this.onLocaleChange});

  @override
  State<AnecdotePage> createState() => _AnecdotePageState();
}

class _AnecdotePageState extends State<AnecdotePage> {
  late FactService factService;
  late TranslateService translateService;
  late PreferencesService prefsService;
  late DailyFactCache dailyCache;
  Timer? _midnightTimer;

  Fact? fact;
  bool isLoading = true;
  bool showAnecdote = false;
  bool showDetails = false;
  bool translated = false;
  String displayedText = '';
  String language = 'en';

  @override
  void initState() {
    super.initState();
    factService = FactService(apiKey: 'hsXlM6fqeIOFEVrkhjOYM7iISwCFnkcuHAEP3556');
    translateService = TranslateService(); 
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
      _loadDailyFact(); // recharge l’anecdote du nouveau jour
      _scheduleMidnightReset(); // réinitialise le timer pour le jour suivant
    });
  }

  Future<void> _loadLanguagePreference() async {
    final lang = await prefsService.getLanguagePreference();
    setState(() {
      language = lang;
    });
    widget.onLocaleChange?.call(Locale(lang));
  }

  Future<void> _loadDailyFact() async {
    setState(() => isLoading = true);

    try {
      final cached = await dailyCache.getTodayFact();

      if (cached != null) {
        setState(() {
          displayedText = language == 'fr' && cached['translated'] != null
              ? cached['translated']
              : cached['original'];
          fact = Fact(text: cached['original']);
          translated = language == 'fr' && cached['translated'] != null;
          showAnecdote = true;
          isLoading = false;
        });
      } else {
        final fetchedFact = await factService.fetchFactOfTheDay();
        String textToShow = fetchedFact.text;
        bool isTranslated = false;

        if (language == 'fr') {
          textToShow = await translateService.translate(fetchedFact.text);
          isTranslated = true;
        }

        await dailyCache.saveTodayFact(
          original: fetchedFact.text,
          translated: isTranslated ? textToShow : null,
        );

        setState(() {
          fact = fetchedFact;
          displayedText = textToShow;
          translated = isTranslated;
          showAnecdote = true;
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        displayedText = 'Error: $e';
        showAnecdote = true;
        isLoading = false;
      });
    }
  }

  Future<void> translateFact() async {
    if (fact == null) return;

    setState(() => isLoading = true);

    try {
      final translation = await translateService.translate(fact!.text);
      await prefsService.saveLanguagePreference('fr');
      await dailyCache.saveTodayFact(original: fact!.text, translated: translation);

      setState(() {
        displayedText = translation;
        translated = true;
        isLoading = false;
        language = 'fr';
      });

      widget.onLocaleChange?.call(const Locale('fr'));
    } catch (e) {
      setState(() {
        displayedText = 'Translation error: $e';
        isLoading = false;
      });
    }
  }

  Future<void> changeLanguage(String lang) async {
    setState(() => isLoading = true);

    await prefsService.saveLanguagePreference(lang);

    setState(() {
      language = lang;
      translated = (lang == 'fr' && fact != null);
      if (lang == 'en' && fact != null) {
        displayedText = fact!.text;
      }
      isLoading = false;
    });

    widget.onLocaleChange?.call(Locale(lang));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: theme.colorScheme.background,
      appBar: AppBar(
        title: const Text('Anecdote of the Day'),
        centerTitle: true,
        backgroundColor: theme.colorScheme.primary,
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language),
            onSelected: changeLanguage,
            itemBuilder: (context) => const [
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
                    const SizedBox(height: 12),
                    if (!translated && language == 'fr')
                      ElevatedButton(
                        onPressed: translateFact,
                        child: const Text('Translate'),
                      ),
                  ],
                ),
              ),
      ),
    );
  }
}
