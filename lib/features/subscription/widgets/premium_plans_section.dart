import 'package:flutter/material.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import '../../../generated/app_localizations.dart';
import 'premium_plan_card.dart';

class PremiumPlansSection extends StatelessWidget {
  final List<Package> packages;
  final Package? selected;
  final ValueChanged<Package> onSelect;
  final VoidCallback onPurchase;
  final VoidCallback onRestore;
  final bool purchasing;
  final bool restoring;

  const PremiumPlansSection({
    super.key,
    required this.packages,
    required this.selected,
    required this.onSelect,
    required this.onPurchase,
    required this.onRestore,
    required this.purchasing,
    required this.restoring,
  });

  static const _amber = Color(0xFFFFB300);

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final theme = Theme.of(context);

    return Column(
      children: [
        if (packages.isEmpty)
          Center(
            child: Text(
              loc.premiumErrorLoading,
              style: TextStyle(color: theme.colorScheme.outline),
            ),
          )
        else
          ...packages.map(
            (p) => PremiumPlanCard(
              package: p,
              isSelected: selected == p,
              isBestValue: p.packageType == PackageType.annual,
              onTap: () => onSelect(p),
            ),
          ),
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          height: 52,
          child: ElevatedButton(
            onPressed: (purchasing || packages.isEmpty) ? null : onPurchase,
            style: ElevatedButton.styleFrom(
              backgroundColor: _amber,
              foregroundColor: Colors.white,
              disabledBackgroundColor: _amber.withValues(alpha: 0.5),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(14),
              ),
            ),
            child: purchasing
                ? const SizedBox(
                    width: 22,
                    height: 22,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      color: Colors.white,
                    ),
                  )
                : Text(
                    loc.premiumCta,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
          ),
        ),
        const SizedBox(height: 12),
        Center(
          child: TextButton(
            onPressed: restoring ? null : onRestore,
            child: restoring
                ? const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : Text(loc.premiumRestore),
          ),
        ),
      ],
    );
  }
}
