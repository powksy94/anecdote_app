import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class PremiumActiveBadge extends StatelessWidget {
  final VoidCallback onManageTap;

  const PremiumActiveBadge({super.key, required this.onManageTap});

  static const _amber = Color(0xFFFFB300);

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: _amber.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: _amber),
      ),
      child: Column(
        children: [
          const Icon(Icons.check_circle_rounded, color: _amber, size: 44),
          const SizedBox(height: 12),
          Text(
            loc.premiumActive,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          OutlinedButton.icon(
            onPressed: onManageTap,
            icon: const Icon(Icons.open_in_new_rounded, size: 16),
            label: Text(loc.premiumManage),
            style: OutlinedButton.styleFrom(
              foregroundColor: _amber,
              side: const BorderSide(color: _amber),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
