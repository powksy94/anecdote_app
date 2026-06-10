import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../../generated/app_localizations.dart';
import '../pages/content_page.dart';

class SubCategoryCard extends StatelessWidget {
  final ContentType type;
  final VoidCallback? onNavigate;

  const SubCategoryCard({super.key, required this.type, this.onNavigate});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: GestureDetector(
        onTap: onNavigate ?? () => Navigator.push(
          context,
          PageRouteBuilder(
            pageBuilder: (_, __, ___) => ContentPage(contentType: type),
            transitionsBuilder: (_, animation, __, child) =>
                FadeTransition(opacity: animation, child: child),
            transitionDuration: const Duration(milliseconds: 250),
          ),
        ),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          decoration: BoxDecoration(
            gradient: LinearGradient(colors: type.gradient),
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: type.accentColor.withValues(alpha: 0.4),
                blurRadius: 16,
                offset: const Offset(0, 6),
              ),
            ],
          ),
          child: Row(
            children: [
              Icon(type.icon, color: Colors.white, size: 32),
              const SizedBox(width: 16),
              Text(
                type.localizedTitle(loc),
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const Spacer(),
              const Icon(
                Icons.arrow_forward_ios_rounded,
                color: Colors.white,
                size: 16,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
