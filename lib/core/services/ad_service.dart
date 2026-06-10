import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/env.dart';

class AdService {
  static const String _keyLastAd = 'last_ad_timestamp';
  static const Duration _interval = Duration(minutes: 20);

  InterstitialAd? _interstitialAd;
  bool _isAdLoaded = false;

  void loadInterstitialAd() {
    InterstitialAd.load(
      adUnitId: Env.admobInterstitialId,
      request: const AdRequest(),
      adLoadCallback: InterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          _interstitialAd = ad;
          _isAdLoaded = true;
        },
        onAdFailedToLoad: (error) {
          debugPrint('InterstitialAd failed to load: $error');
          _isAdLoaded = false;
        },
      ),
    );
  }

  Future<bool> canShowAd() async {
    final prefs = await SharedPreferences.getInstance();
    final lastMs = prefs.getInt(_keyLastAd) ?? 0;
    final elapsed = DateTime.now().millisecondsSinceEpoch - lastMs;
    return elapsed >= _interval.inMilliseconds;
  }

  Future<void> _recordAdShown() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_keyLastAd, DateTime.now().millisecondsSinceEpoch);
  }

  Future<void> showInterstitialAd({required VoidCallback onComplete}) async {
    final allowed = await canShowAd();
    if (!allowed || !_isAdLoaded || _interstitialAd == null) {
      onComplete();
      return;
    }

    await _recordAdShown();
    _interstitialAd!.fullScreenContentCallback = FullScreenContentCallback(
      onAdDismissedFullScreenContent: (ad) {
        ad.dispose();
        _interstitialAd = null;
        _isAdLoaded = false;
        onComplete();
        loadInterstitialAd();
      },
      onAdFailedToShowFullScreenContent: (ad, error) {
        ad.dispose();
        _interstitialAd = null;
        _isAdLoaded = false;
        onComplete();
      },
    );
    _interstitialAd!.show();
  }

  void dispose() {
    _interstitialAd?.dispose();
  }
}
