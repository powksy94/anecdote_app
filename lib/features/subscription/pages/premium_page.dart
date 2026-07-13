import 'package:flutter/material.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import '../../../generated/app_localizations.dart';
import '../services/purchase_service.dart';
import '../widgets/premium_active_badge.dart';
import '../widgets/premium_benefit_tile.dart';
import '../widgets/premium_header.dart';
import '../widgets/premium_plans_section.dart';

class PremiumPage extends StatefulWidget {
  const PremiumPage({super.key});

  @override
  State<PremiumPage> createState() => _PremiumPageState();
}

class _PremiumPageState extends State<PremiumPage> {
  Offerings? _offerings;
  bool _loading = true;
  bool _isPremium = false;
  Package? _selected;
  bool _purchasing = false;
  bool _restoring = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final results = await Future.wait([
      PurchaseService.getOfferings(),
      PurchaseService.isPremium(),
    ]);
    if (!mounted) return;
    final offerings = results[0] as Offerings?;
    setState(() {
      _offerings = offerings;
      _isPremium = results[1] as bool;
      _loading = false;
      _selected = offerings?.current?.annual ?? offerings?.current?.monthly;
    });
  }

  Future<void> _purchase() async {
    if (_selected == null || _purchasing) return;
    setState(() => _purchasing = true);
    try {
      final success = await PurchaseService.purchasePackage(_selected!);
      if (mounted && success) setState(() => _isPremium = true);
    } on PurchasesError catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message)),
        );
      }
    } finally {
      if (mounted) setState(() => _purchasing = false);
    }
  }

  Future<void> _restore() async {
    setState(() => _restoring = true);
    final success = await PurchaseService.restorePurchases();
    if (!mounted) return;
    final loc = AppLocalizations.of(context)!;
    setState(() {
      _restoring = false;
      if (success) _isPremium = true;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          success ? loc.premiumRestoreSuccess : loc.premiumRestoreEmpty,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final packages = _offerings?.current?.availablePackages ?? [];

    return Scaffold(
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : CustomScrollView(
              slivers: [
                SliverToBoxAdapter(
                  child: Stack(
                    children: [
                      const PremiumHeader(),
                      const Positioned(
                        top: 48,
                        left: 8,
                        child: BackButton(color: Colors.white),
                      ),
                    ],
                  ),
                ),
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(24, 28, 24, 32),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        PremiumBenefitTile(
                          icon: Icons.bookmark_rounded,
                          label: loc.premiumBenefitFavorites,
                        ),
                        PremiumBenefitTile(
                          icon: Icons.block_rounded,
                          label: loc.premiumBenefitAds,
                        ),
                        PremiumBenefitTile(
                          icon: Icons.rocket_launch_rounded,
                          label: loc.premiumBenefitContent,
                        ),
                        const SizedBox(height: 28),
                        if (_isPremium)
                          PremiumActiveBadge(
                            onManageTap: PurchaseService.manageSubscriptions,
                          )
                        else
                          PremiumPlansSection(
                            packages: packages,
                            selected: _selected,
                            onSelect: (p) => setState(() => _selected = p),
                            onPurchase: _purchase,
                            onRestore: _restore,
                            purchasing: _purchasing,
                            restoring: _restoring,
                          ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
    );
  }
}
