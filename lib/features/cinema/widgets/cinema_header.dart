import 'package:flutter/material.dart';

class CinemaHeader extends StatelessWidget {
  final List<Color> gradient;
  final IconData icon;

  const CinemaHeader({super.key, required this.gradient, required this.icon});

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: gradient),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Icon(icon, size: 40, color: Colors.white),
      );
}
