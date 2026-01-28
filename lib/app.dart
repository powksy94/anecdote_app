import 'package:flutter/material.dart';
import 'pages/anecdote_page.dart';

class AnecdoteApp extends StatelessWidget {
  const AnecdoteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Anecdote du jour',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: const AnecdotePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
