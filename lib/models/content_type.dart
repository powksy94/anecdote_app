import 'package:flutter/material.dart';
import '../generated/app_localizations.dart';

enum ContentType {
  anecdote,
  chuckNorris,
  advice,
  history,
  animals,
}

extension ContentTypeExtension on ContentType {
  String get title {
    switch (this) {
      case ContentType.anecdote:
        return 'Anecdote';
      case ContentType.chuckNorris:
        return 'Chuck Norris';
      case ContentType.advice:
        return 'Advice';
      case ContentType.history:
        return 'History';
      case ContentType.animals:
        return 'Animals';
    }
  }

  String localizedTitle(AppLocalizations loc) {
    switch (this) {
      case ContentType.anecdote:
        return loc.categoryAnecdote;
      case ContentType.chuckNorris:
        return loc.categoryChuckNorris;
      case ContentType.advice:
        return loc.categoryAdvice;
      case ContentType.history:
        return loc.categoryHistory;
      case ContentType.animals:
        return loc.categoryAnimals;
    }
  }

  IconData get icon {
    switch (this) {
      case ContentType.anecdote:
        return Icons.lightbulb_rounded;
      case ContentType.chuckNorris:
        return Icons.sports_martial_arts_rounded;
      case ContentType.advice:
        return Icons.psychology_rounded;
      case ContentType.history:
        return Icons.auto_stories_rounded;
      case ContentType.animals:
        return Icons.pets_rounded;
    }
  }

  Color get color {
    switch (this) {
      case ContentType.anecdote:
        return Colors.indigo;
      case ContentType.chuckNorris:
        return Colors.red;
      case ContentType.advice:
        return Colors.teal;
      case ContentType.history:
        return Colors.amber.shade700;
      case ContentType.animals:
        return Colors.green;
    }
  }

  List<Color> get gradient {
    switch (this) {
      case ContentType.anecdote:
        return [const Color(0xFF667eea), const Color(0xFF764ba2)];
      case ContentType.chuckNorris:
        return [const Color(0xFFf85032), const Color(0xFFe73827)];
      case ContentType.advice:
        return [const Color(0xFF11998e), const Color(0xFF38ef7d)];
      case ContentType.history:
        return [const Color(0xFFf2994a), const Color(0xFFf2c94c)];
      case ContentType.animals:
        return [const Color(0xFF56ab2f), const Color(0xFFa8e063)];
    }
  }

  String get apiEndpoint {
    switch (this) {
      case ContentType.anecdote:
        return 'https://api.api-ninjas.com/v1/facts';
      case ContentType.chuckNorris:
        return 'https://api.api-ninjas.com/v1/chucknorris';
      case ContentType.advice:
        return 'https://api.api-ninjas.com/v1/quotes?category=inspirational';
      case ContentType.history:
        return 'https://api.api-ninjas.com/v1/historicalevents';
      case ContentType.animals:
        return 'https://api.api-ninjas.com/v1/animals?name=lion';
    }
  }
}
