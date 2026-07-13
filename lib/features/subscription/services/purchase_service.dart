import 'dart:async';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:url_launcher/url_launcher.dart';

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
    late StreamController<bool> controller;

    void listener(CustomerInfo info) {
      if (!controller.isClosed) {
        controller.add(info.entitlements.active.containsKey(_entitlementId));
      }
    }

    controller = StreamController<bool>(
      onListen: () async {
        try {
          final info = await Purchases.getCustomerInfo();
          if (!controller.isClosed) {
            controller.add(info.entitlements.active.containsKey(_entitlementId));
          }
        } catch (_) {
          if (!controller.isClosed) controller.add(false);
        }
        Purchases.addCustomerInfoUpdateListener(listener);
      },
      onCancel: () {
        Purchases.removeCustomerInfoUpdateListener(listener);
      },
    );

    return controller.stream;
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

  static Future<void> manageSubscriptions() async {
    final uri = Uri.parse('https://play.google.com/store/account/subscriptions');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }
}
