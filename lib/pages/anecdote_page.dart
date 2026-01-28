import 'package:flutter/material.dart';
import '../services/fact_service.dart';
import '../widgets/anecdote_card.dart';
import '../models/fact.dart';

class AnecdotePage extends StatefulWidget {
  const AnecdotePage({super.key});

  @override
  State<AnecdotePage> createState() => _AnecdotePageState();
}

class _AnecdotePageState extends State<AnecdotePage> {
  late FactService factService;
  Fact? fact;
  bool isLoading = true;
  bool showDetails = false;

  @override
  void initState() {
    super.initState();
    factService = FactService(apiKey: 'YOUR_API_KEY_HERE');
    loadFact();
  }

  Future<void> loadFact() async {
    try {
      final fetchedFact = await factService.fetchFactOfTheDay();
      setState(() {
        fact = fetchedFact;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        fact = Fact(text: 'Erreur: $e');
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Anecdote du jour'),
        centerTitle: true,
      ),
      body: Center(
        child: isLoading
            ? const CircularProgressIndicator()
            : AnecdoteCard(
                text: fact!.text,
                showDetails: showDetails,
                onTap: () => setState(() => showDetails = !showDetails),
              ),
      ),
    );
  }
}
