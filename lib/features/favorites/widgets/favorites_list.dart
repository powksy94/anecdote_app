import 'package:flutter/material.dart';
import '../models/favorite_fact.dart';
import '../services/favorites_service.dart';
import 'favorite_card.dart';
import 'favorites_empty_state.dart';

class FavoritesList extends StatelessWidget {
  final List<FavoriteFact> facts;
  final String uid;

  const FavoritesList({
    super.key,
    required this.facts,
    required this.uid,
  });

  @override
  Widget build(BuildContext context) {
    if (facts.isEmpty) return const FavoritesEmptyState();

    return ListView.builder(
      itemCount: facts.length,
      padding: const EdgeInsets.only(bottom: 24),
      itemBuilder: (_, i) => FavoriteCard(
        fact: facts[i],
        onDelete: () => FavoritesService(uid).toggle(facts[i]),
      ),
    );
  }
}
