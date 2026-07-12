import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../generated/app_localizations.dart';

class FavoritesFilterBar extends StatelessWidget {
  final List<ContentType> categories;
  final ContentType? selected;
  final void Function(ContentType? cat) onSelect;

  const FavoritesFilterBar({
    super.key,
    required this.categories,
    required this.selected,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          FilterChip(
            label: Text(loc.filterAll),
            selected: selected == null,
            onSelected: (_) => onSelect(null),
          ),
          const SizedBox(width: 8),
          ...categories.map((cat) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: FilterChip(
                  avatar: Icon(cat.icon, size: 16),
                  label: Text(cat.localizedTitle(loc)),
                  selected: selected == cat,
                  onSelected: (_) =>
                      onSelect(selected == cat ? null : cat),
                ),
              )),
        ],
      ),
    );
  }
}
