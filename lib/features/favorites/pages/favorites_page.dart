import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../core/models/content_type.dart';
import '../models/favorite_fact.dart';
import '../services/favorites_service.dart';
import '../widgets/favorites_filter_bar.dart';
import '../widgets/favorites_header.dart';
import '../widgets/favorites_list.dart';

class FavoritesPage extends StatefulWidget {
  const FavoritesPage({super.key});

  @override
  State<FavoritesPage> createState() => _FavoritesPageState();
}

class _FavoritesPageState extends State<FavoritesPage> {
  ContentType? _selectedCategory;

  String get _uid => FirebaseAuth.instance.currentUser!.uid;

  String _monthLabel(BuildContext context) {
    final locale = Localizations.localeOf(context).languageCode;
    return DateFormat.yMMMM(locale).format(DateTime.now());
  }

  List<FavoriteFact> _filtered(List<FavoriteFact> all) {
    if (_selectedCategory == null) return all;
    return all.where((f) => f.contentType == _selectedCategory).toList();
  }

  List<ContentType> _categories(List<FavoriteFact> all) =>
      all.map((f) => f.contentType).toSet().toList();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: StreamBuilder<List<FavoriteFact>>(
          stream: FavoritesService(_uid).watchAll(),
          builder: (context, snapshot) {
            final all = snapshot.data ?? [];
            final filtered = _filtered(all);
            final categories = _categories(all);

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                FavoritesHeader(
                  monthLabel: _monthLabel(context),
                  count: all.length,
                ),
                if (categories.isNotEmpty)
                  FavoritesFilterBar(
                    categories: categories,
                    selected: _selectedCategory,
                    onSelect: (cat) =>
                        setState(() => _selectedCategory = cat),
                  ),
                Expanded(
                  child: snapshot.connectionState ==
                          ConnectionState.waiting
                      ? const Center(child: CircularProgressIndicator())
                      : FavoritesList(facts: filtered, uid: _uid),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
