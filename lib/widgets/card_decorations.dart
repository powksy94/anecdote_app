import 'package:flutter/material.dart';
import '../models/content_type.dart';

Widget buildCardDecoration(ContentType type) {
  switch (type) {
    // --- Modèle Stars : cercles + icônes étoiles ---
    case ContentType.anecdote:
      return _anecdoteDecoration();
    case ContentType.space:
    case ContentType.exoplanet:
      return _stars(count: 3);

    // --- Modèle Rects : rectangles pivotés + icône ---
    case ContentType.chuckNorris:
      return _rects(Icons.bolt);
    case ContentType.history:
      return _historyDecoration();

    // --- Modèle Bubbles : bulles + icône (quote) ---
    case ContentType.celebrityQuote:
      return _bubbles(Icons.format_quote);

    // --- Modèle DoubleIcon : 2 cercles + 2 icônes ---
    case ContentType.animals:
      return _doubleIcon(Icons.eco, Icons.eco);
    case ContentType.country:
      return _doubleIcon(Icons.public, Icons.location_on);
    case ContentType.world:
      return _doubleIcon(Icons.travel_explore, Icons.pin_drop);

    // --- Modèle SingleIcon : 2 cercles + 1 icône ---
    case ContentType.frenchDepartment:
      return _singleIcon(Icons.location_city);
    case ContentType.pacificIsland:
      return _singleIcon(Icons.waves);
    case ContentType.historyHub:
      return _singleIcon(Icons.history_edu);
    case ContentType.celebrityHub:
      return _bubbles(Icons.stars);
    case ContentType.scienceHub:
      return _doubleIcon(Icons.science, Icons.eco);
    case ContentType.spaceMission:
      return _singleIcon(Icons.rocket, iconSize: 16);
    case ContentType.battle:
      return _doubleIcon(Icons.shield, Icons.local_fire_department);
    case ContentType.dinosaur:
      return _singleIcon(Icons.rowing_rounded, iconSize: 16);
    case ContentType.cinemaHub:
      return _doubleIcon(Icons.movie, Icons.star);
    case ContentType.classicCinema:
      return _rects(Icons.theaters);
    case ContentType.cinema80s90s:
      return _singleIcon(Icons.videocam, iconSize: 16);
    case ContentType.modernCinema:
      return _singleIcon(Icons.local_movies);
    case ContentType.kingOfFrance:
      return _singleIcon(Icons.castle);
    case ContentType.americanPresident:
      return _singleIcon(Icons.account_balance);
    case ContentType.star:
      return _singleIcon(Icons.star, iconSize: 16);
    case ContentType.solarSystemMoon:
      return _singleIcon(Icons.brightness_2);
    case ContentType.artHub:
      return _doubleIcon(Icons.palette, Icons.brush);
    case ContentType.painting:
      return _singleIcon(Icons.brush, iconSize: 16);
    case ContentType.frenchCommune:
      return _doubleIcon(Icons.location_city, Icons.flag);
    case ContentType.americanState:
      return _doubleIcon(Icons.flag, Icons.location_on);
  }
}

// ── Builders privés ────────────────────────────────────────────────────────

Widget _anecdoteDecoration() => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(60, Colors.white.withValues(alpha: 0.10))),
        Positioned(bottom: -30, left: -30, child: _circle(80, Colors.white.withValues(alpha: 0.08))),
        Positioned(top: 20, left: 10, child: _icon(Icons.star, 12, 0.30)),
        Positioned(bottom: 40, right: 20, child: _icon(Icons.star, 8, 0.25)),
      ],
    );

Widget _historyDecoration() => Stack(
      children: [
        Positioned(
          top: 10, right: -20,
          child: Transform.rotate(angle: 0.2, child: _rect(60, 20, Colors.white.withValues(alpha: 0.10))),
        ),
        Positioned(
          bottom: 20, left: -15,
          child: Transform.rotate(angle: -0.15, child: _rect(50, 15, Colors.white.withValues(alpha: 0.08))),
        ),
        Positioned(top: 50, left: 15, child: _icon(Icons.access_time, 12, 0.30)),
      ],
    );

Widget _stars({required int count}) => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(65, Colors.white.withValues(alpha: 0.07))),
        Positioned(bottom: -15, left: -15, child: _circle(45, Colors.white.withValues(alpha: 0.09))),
        Positioned(top: 12, left: 14, child: _icon(Icons.star, 8, 0.30)),
        Positioned(bottom: 30, right: 14, child: _icon(Icons.star, 5, 0.20)),
        if (count >= 3)
          Positioned(top: 40, right: 8, child: _icon(Icons.star, 6, 0.25)),
      ],
    );

Widget _rects(IconData icon) => Stack(
      children: [
        Positioned(
          top: -15, left: -15,
          child: Transform.rotate(angle: 0.3, child: _rect(50, 50, Colors.white.withValues(alpha: 0.1))),
        ),
        Positioned(
          bottom: -20, right: -10,
          child: Transform.rotate(angle: -0.5, child: _rect(40, 40, Colors.white.withValues(alpha: 0.08))),
        ),
        Positioned(top: 15, right: 15, child: _icon(icon, 14, 0.3)),
      ],
    );

Widget _bubbles(IconData icon) => Stack(
      children: [
        Positioned(top: -25, right: 20, child: _circle(50, Colors.white.withValues(alpha: 0.12))),
        Positioned(bottom: -15, left: 30, child: _circle(35, Colors.white.withValues(alpha: 0.10))),
        Positioned(top: 40, left: 5, child: _circle(15, Colors.white.withValues(alpha: 0.15))),
        Positioned(bottom: 30, right: 10, child: _icon(icon, 16, 0.25)),
      ],
    );

Widget _singleIcon(IconData icon, {double iconSize = 14}) => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(60, Colors.white.withValues(alpha: 0.10))),
        Positioned(bottom: -15, left: -15, child: _circle(50, Colors.white.withValues(alpha: 0.08))),
        Positioned(top: 15, right: 12, child: _icon(icon, iconSize, 0.3)),
      ],
    );

Widget _doubleIcon(IconData icon1, IconData icon2) => Stack(
      children: [
        Positioned(top: -20, left: -20, child: _circle(70, Colors.white.withValues(alpha: 0.08))),
        Positioned(bottom: -15, right: -15, child: _circle(55, Colors.white.withValues(alpha: 0.10))),
        Positioned(top: 15, right: 12, child: _icon(icon1, 14, 0.30)),
        Positioned(bottom: 35, left: 12, child: _icon(icon2, 10, 0.25)),
      ],
    );

// ── Primitives ─────────────────────────────────────────────────────────────

Widget _circle(double size, Color color) => Container(
      width: size,
      height: size,
      decoration: BoxDecoration(shape: BoxShape.circle, color: color),
    );

Widget _rect(double width, double height, Color color) => Container(
      width: width,
      height: height,
      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(8)),
    );

Widget _icon(IconData icon, double size, double opacity) =>
    Icon(icon, size: size, color: Colors.white.withValues(alpha: opacity));
