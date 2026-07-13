import 'package:flutter/material.dart';

class PremiumBenefitTile extends StatelessWidget {
  final IconData icon;
  final String label;

  const PremiumBenefitTile({super.key, required this.icon, required this.label});

  static const _amber = Color(0xFFFFB300);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: _amber.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: _amber, size: 20),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Text(label, style: Theme.of(context).textTheme.bodyMedium),
          ),
        ],
      ),
    );
  }
}
