import 'dart:math';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

void main() {
  runApp(const AnecdoteApp());
}

class AnecdoteApp extends StatelessWidget {
  const AnecdoteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Anecdote du jour',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: const AnecdotePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class AnecdotePage extends StatefulWidget {
  const AnecdotePage({super.key});

  @override
  State<AnecdotePage> createState() => _AnecdotePageState();
}

class _AnecdotePageState extends State<AnecdotePage> {
  final Map<String, String> anecdotes = const {
    "Les fourmis n'ont pas de poumons.":
        "Elles respirent par de petits trous appelés spiracles situés sur les côtés de leur corps.",
    "La Lune s'éloigne de la Terre de 3,8 cm par an.":
        "Ce phénomène est mesuré avec des lasers envoyés vers des réflecteurs placés sur la Lune.",
    "Le cœur d'une crevette est situé dans sa tête.":
        "Chez la crevette, les organes vitaux sont regroupés dans la tête, protégés par sa carapace.",
    // Ajoute-en autant que tu veux...
  };

  bool showDetails = false;

  String getTodayKey() {
    final today = DateFormat('yyyy-MM-dd').format(DateTime.now());
    final keys = anecdotes.keys.toList();
    final hash = today.hashCode;
    final index = hash.abs() % keys.length;
    return keys[index];
  }

  @override
  Widget build(BuildContext context) {
    final title = getTodayKey();
    final detail = anecdotes[title]!;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Anecdote du jour'),
        centerTitle: true,
      ),
      body: GestureDetector(
        onTap: () => setState(() => showDetails = !showDetails),
        child: Center(
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            padding: const EdgeInsets.all(20),
            constraints: BoxConstraints(
              maxHeight: showDetails ? 300 : 100,
              maxWidth: 400,
            ),
            decoration: BoxDecoration(
              color: Colors.indigo[50],
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(
                  color: Colors.indigo.withOpacity(0.2),
                  blurRadius: 10,
                ),
              ],
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  title,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 12),
                if (showDetails)
                  Text(
                    detail,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 16,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
