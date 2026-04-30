import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../generated/app_localizations.dart';
import '../widgets/subcategory_card.dart';

class WorldPage extends StatelessWidget {
  const WorldPage({super.key});

  static const _subCategories = [ContentType.country];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = ContentType.world.gradient;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(ContentType.world.icon, size: 24),
            const SizedBox(width: 8),
            Text(ContentType.world.localizedTitle(loc)),
          ],
        ),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.arrow_back, size: 20),
          ),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              gradient[0],
              gradient[1].withValues(alpha: 0.8),
              theme.colorScheme.surface,
            ],
            stops: const [0.0, 0.3, 0.6],
          ),
        ),
        child: SafeArea(
          child: ListView.builder(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 24),
            itemCount: _subCategories.length,
            itemBuilder: (context, index) =>
                SubCategoryCard(type: _subCategories[index]),
          ),
        ),
      ),
    );
  }
}
