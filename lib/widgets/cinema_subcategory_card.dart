import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../generated/app_localizations.dart';

const _posterAssets = {
  ContentType.classicCinema: 'assets/the-good-the-bad-and-the-ugly.jpg',
  ContentType.cinema80s90s:  'assets/terminator.jpg',
  ContentType.modernCinema:  'assets/Parasite.jpg',
};

const _posterAlignments = {
  ContentType.classicCinema: Alignment.center,
  ContentType.cinema80s90s:  Alignment(0, -0.4),
  ContentType.modernCinema:  Alignment(0, -0.7),
};

class CinemaSubCategoryCard extends StatelessWidget {
  final ContentType type;
  final VoidCallback? onNavigate;

  const CinemaSubCategoryCard({
    super.key,
    required this.type,
    this.onNavigate,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final posterAsset = _posterAssets[type];

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: GestureDetector(
        onTap: onNavigate,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(20),
          child: SizedBox(
            height: 110,
            child: Stack(
              fit: StackFit.expand,
              children: [
                // Affiche locale en fond
                if (posterAsset != null)
                  Image.asset(
                    posterAsset,
                    fit: BoxFit.cover,
                    alignment: _posterAlignments[type] ?? Alignment.center,
                  )
                else
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(colors: type.gradient),
                    ),
                  ),

                // Overlay semi-transparent
                Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                      colors: [
                        type.gradient[0].withValues(alpha: 0.85),
                        Colors.black.withValues(alpha: 0.5),
                      ],
                    ),
                  ),
                ),

                // Contenu
                Padding(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 24, vertical: 20),
                  child: Row(
                    children: [
                      Icon(type.icon, color: Colors.white, size: 32),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Text(
                          type.localizedTitle(loc),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      const Icon(
                        Icons.arrow_forward_ios_rounded,
                        color: Colors.white,
                        size: 16,
                      ),
                    ],
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
