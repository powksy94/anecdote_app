import 'package:purchases_flutter/purchases_flutter.dart';

const _entitlementId = 'Daily Facts Premium';
const _androidApiKey = 'test_KXLkEEVAurdDHRhYNbAJFWkfTns';

class PurchaseService {
  static Future<void> configure() async {
    await Purchases.configure(PurchasesConfiguration(_androidApiKey));
  }

  static Future<bool> isPremium() async {
    try {
      final info = await Purchases.getCustomerInfo();
      return info.entitlements.active.containsKey(_entitlementId);
    } catch (_) {
      return false;
    }
  }

  static Stream<bool> get premiumStream {
    try {
      return Purchases.customerInfoStream.map(
        (info) => info.entitlements.active.containsKey(_entitlementId),
      );
    } catch (_) {
      return Stream.value(false);
    }
  }

  static Future<Offerings?> getOfferings() async {
    try {
      return await Purchases.getOfferings();
    } catch (_) {
      return null;
    }
  }

  static Future<bool> purchasePackage(Package package) async {
    try {
      final info = await Purchases.purchasePackage(package);
      return info.entitlements.active.containsKey(_entitlementId);
    } on PurchasesError catch (e) {
      if (e.code == PurchasesErrorCode.purchaseCancelledError) return false;
      rethrow;
    }
  }

  static Future<bool> restorePurchases() async {
    try {
      final info = await Purchases.restorePurchases();
      return info.entitlements.active.containsKey(_entitlementId);
    } catch (_) {
      return false;
    }
  }
}
