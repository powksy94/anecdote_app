import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../../generated/app_localizations.dart';

class HubSectionCard extends StatelessWidget {
  final ContentType type;
  final AppLocalizations loc;
  final VoidCallback onTap;

  const HubSectionCard({
    super.key,
    required this.type,
    required this.loc,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final grad = type.gradient;
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [grad[0], grad[1]],
          ),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: grad[0].withValues(alpha: 0.35),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(type.icon, size: 48, color: Colors.white),
            const SizedBox(height: 14),
            Text(
              type.localizedTitle(loc),
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 15,
                fontWeight: FontWeight.bold,
                letterSpacing: 0.3,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
