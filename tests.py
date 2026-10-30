"""Pruebas unitarias para el motor, la narrativa y las campañas de Crónicas de Aethelgard."""

from __future__ import annotations

import random
import unittest

from cronicas import lore
from cronicas.engine import (
    ALL_COLORS, AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FAIRY_KINDS,
    FALCON, GRASSHOPPER, GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX,
    QUEEN, RED, ROOK, WHITE, ZEBRA, Game, Move, Piece, evaluate,
    find_best_move, move_notation,
)


class EngineRulesTests(unittest.TestCase):
    def test_classic_setup_and_initial_moves(self) -> None:
        game = lore.create_game()
        self.assertEqual(len(game.legal_moves(WHITE)), 20)
        self.assertEqual(len(game.legal_moves(BLACK)), 20)
        self.assertFalse(game.in_check(WHITE))
        # Solo el Rey y la Reina tienen nombres propios reales; el resto usa el nombre de la pieza
        self.assertEqual(game.piece_at(7, 4).name, "Rey Balduino")
        self.assertEqual(game.piece_at(7, 3).name, "Reina Leonor")
        self.assertEqual(game.piece_at(0, 4).name, "Rey Vladimir")
        self.assertEqual(game.piece_at(0, 3).name, "Reina Carmila")
        self.assertEqual(game.piece_at(7, 0).name, "Torre")
        self.assertEqual(game.piece_at(7, 1).name, "Caballo")
        self.assertEqual(game.piece_at(7, 2).name, "Alfil")
        self.assertEqual(game.piece_at(6, 0).name, "Peón")

    def test_elephant_setup_and_leap_moves(self) -> None:
        game = lore.create_game(elephant=True)
        piece = game.piece_at(7, 2)
        self.assertIsNotNone(piece)
        assert piece is not None
        self.assertEqual(piece.kind, ELEPHANT)
        # El elefante (Torre + Caballo) salta sobre los peones en la jugada inicial (7,2) -> (5,1) y (5,3)
        moves = game.legal_moves_from(7, 2)
        targets = {(m.tr, m.tc) for m in moves}
        self.assertEqual(targets, {(5, 1), (5, 3)})

    def test_all_ten_fairy_pieces_mechanics(self) -> None:
        # 1. Halcón (Alfil + Caballo)
        g = Game()
        g.place(Piece(WHITE, KING, 1, "Rey"), 7, 4)
        g.place(Piece(BLACK, KING, 2, "Rey"), 0, 4)
        g.place(Piece(WHITE, FALCON, 3, "Halcón"), 4, 4)
        targets = {(m.tr, m.tc) for m in g.legal_moves_from(4, 4)}
        self.assertIn((2, 2), targets)  # diagonal (Alfil)
        self.assertIn((2, 3), targets)  # salto (Caballo)

        # 2. Amazonas (Reina + Caballo)
        g.place(Piece(WHITE, AMAZON, 3, "Amazonas"), 4, 4)
        targets = {(m.tr, m.tc) for m in g.legal_moves_from(4, 4)}
        self.assertIn((4, 0), targets)  # ortogonal
        self.assertIn((1, 1), targets)  # diagonal
        self.assertIn((2, 5), targets)  # salto de caballo

        # 3. Saltamontes (salta sobre la primera pieza y aterriza inmediatamente detrás)
        g_hop = Game()
        g_hop.place(Piece(WHITE, KING, 1, "Rey"), 7, 0)
        g_hop.place(Piece(BLACK, KING, 2, "Rey"), 0, 7)
        g_hop.place(Piece(WHITE, GRASSHOPPER, 3, "Saltamontes"), 4, 4)
        g_hop.place(Piece(WHITE, PAWN, 4, "Obstáculo"), 4, 6)
        g_hop.place(Piece(BLACK, PAWN, 5, "Enemigo"), 2, 4)
        hop_targets = {(m.tr, m.tc) for m in g_hop.legal_moves_from(4, 4)}
        self.assertEqual(hop_targets, {(4, 7), (1, 4)})

        # 4. León (salta sobre una pieza y aterriza en cualquier casilla posterior de la línea)
        g_hop.place(Piece(WHITE, LION, 3, "León"), 4, 4)
        lion_targets = {(m.tr, m.tc) for m in g_hop.legal_moves_from(4, 4)}
        self.assertEqual(lion_targets, {(4, 7), (1, 4), (0, 4)})

        # 5. Noctámbulo (saltos consecutivos de caballo en la misma dirección)
        g_nr = Game()
        g_nr.place(Piece(WHITE, KING, 1, "Rey"), 7, 4)
        g_nr.place(Piece(BLACK, KING, 2, "Rey"), 0, 4)
        g_nr.place(Piece(WHITE, NIGHTRIDER, 3, "Noctámbulo"), 7, 1)
        nr_targets = {(m.tr, m.tc) for m in g_nr.legal_moves_from(7, 1)}
        self.assertIn((5, 2), nr_targets)
        self.assertIn((3, 3), nr_targets)
        self.assertIn((1, 4), nr_targets)

        # 6. Centauro (Rey + Caballo), Camello (3,1), Cebra (3,2) y Fénix (1 paso ortogonal + salto 2,2)
        g_misc = Game()
        g_misc.place(Piece(WHITE, KING, 1, "Rey"), 7, 4)
        g_misc.place(Piece(BLACK, KING, 2, "Rey"), 0, 4)
        g_misc.place(Piece(WHITE, CENTAUR, 3, "Centauro"), 4, 4)
        self.assertEqual(len(g_misc.legal_moves_from(4, 4)), 16)

        g_misc.place(Piece(WHITE, CAMEL, 3, "Camello"), 4, 4)
        camel_targets = {(m.tr, m.tc) for m in g_misc.legal_moves_from(4, 4)}
        self.assertIn((1, 3), camel_targets)
        self.assertIn((7, 5), camel_targets)

        g_misc.place(Piece(WHITE, ZEBRA, 3, "Cebra"), 4, 4)
        zebra_targets = {(m.tr, m.tc) for m in g_misc.legal_moves_from(4, 4)}
        self.assertIn((1, 2), zebra_targets)
        self.assertIn((7, 6), zebra_targets)

        g_misc.place(Piece(WHITE, PHOENIX, 3, "Fénix"), 4, 4)
        phoenix_targets = {(m.tr, m.tc) for m in g_misc.legal_moves_from(4, 4)}
        self.assertEqual(
            phoenix_targets,
            {(3, 4), (5, 4), (4, 3), (4, 5), (2, 2), (2, 6), (6, 2), (6, 6)},
        )

    def test_terrain_blocks_sliding_and_stepping(self) -> None:
        game = Game()
        game.place(Piece(WHITE, KING, 1, "Rey"), 7, 4)
        game.place(Piece(BLACK, KING, 2, "Rey"), 0, 4)
        game.place(Piece(WHITE, ROOK, 3, "Torre"), 4, 4)
        # Peñasco es impasable; Bosque permite entrar pero frena el deslizamiento detrás
        game.add_terrain("penasco", 4, 2)
        game.add_terrain("bosque", 4, 6)

        moves = game.legal_moves_from(4, 4)
        targets = {(m.tr, m.tc) for m in moves}
        self.assertIn((4, 3), targets)
        self.assertNotIn((4, 2), targets)
        self.assertNotIn((4, 1), targets)
        # La torre puede entrar al bosque (4,6), pero no pasar a (4,7)
        self.assertIn((4, 6), targets)
        self.assertNotIn((4, 7), targets)

    def test_fortified_ruins_and_veteran_promotion(self) -> None:
        game = Game()
        game.place(Piece(WHITE, KING, 1, "Rey"), 7, 4)
        game.place(Piece(BLACK, KING, 2, "Rey"), 0, 4)
        game.place(Piece(WHITE, ROOK, 3, "Bastión Aurum"), 4, 0)
        game.place(Piece(BLACK, PAWN, 4, "Varok"), 4, 5)
        game.add_terrain("ruinas", 4, 5)

        # La ruina protege contra capturas a más de 1 casilla de distancia
        targets_far = {(m.tr, m.tc) for m in game.legal_moves_from(4, 0)}
        self.assertNotIn((4, 5), targets_far)

        # Pero a distancia 1 sí puede capturar
        game.place(Piece(WHITE, ROOK, 3, "Bastión Aurum", kills=1), 4, 4)
        game.grid[4][0] = None
        moves_adj = [m for m in game.legal_moves_from(4, 4) if (m.tr, m.tc) == (4, 5)]
        self.assertEqual(len(moves_adj), 1)
        game.apply_move(moves_adj[0])
        promoted_rook = game.piece_at(4, 5)
        self.assertIsNotNone(promoted_rook)
        assert promoted_rook is not None
        self.assertEqual(promoted_rook.kills, 2)
        self.assertTrue(promoted_rook.veteran)

    def test_fog_of_war_visibility(self) -> None:
        game = lore.create_game()
        visible = game.visible_squares(WHITE)
        # Las filas propias (6 y 7) y las casillas vigiladas en la fila 5 son visibles
        for c in range(8):
            self.assertIn((7, c), visible)
            self.assertIn((6, c), visible)
            self.assertIn((5, c), visible)
            self.assertNotIn((0, c), visible)

    def test_ai_search_returns_legal_move(self) -> None:
        game = lore.create_game(elephant=True)
        move = find_best_move(game, depth=2, randomness=0.0, time_limit=1.0, rng=random.Random(42))
        self.assertIsNotNone(move)
        assert move is not None
        legal_coords = {(m.fr, m.fc, m.tr, m.tc, m.promotion) for m in game.legal_moves(WHITE)}
        self.assertIn((move.fr, move.fc, move.tr, move.tc, move.promotion), legal_coords)
        notation = move_notation(move)
        self.assertTrue(len(notation) >= 2)
        self.assertIsInstance(evaluate(game), int)


class LoreAndWildsTests(unittest.TestCase):
    def test_wild_scenario_generation_classic_and_elephant(self) -> None:
        rng = random.Random(12345)
        scenario = lore.create_wild_scenario(rng=rng, elephant=True)
        self.assertIsNotNone(scenario.game)
        self.assertGreaterEqual(len(scenario.game.terrain), 6)
        self.assertTrue(scenario.game.legal_moves(WHITE))
        self.assertTrue(scenario.game.legal_moves(BLACK))

        elephants = [
            p for row in scenario.game.grid for p in row
            if p is not None and p.kind == ELEPHANT
        ]
        self.assertGreaterEqual(len(elephants), 2)

        intro = lore.wild_prologue(scenario, vs_ai=True, difficulty="Caballero", fog=True)
        self.assertIn("niebla de guerra", intro.text)

        event = lore.wild_event(scenario.game, scenario, rng=rng)
        self.assertIsNotNone(event)

        dilemma = lore.wild_dilemma(scenario.game, scenario, rng=rng)
        self.assertIsNotNone(dilemma)
        assert dilemma is not None
        self.assertEqual(len(dilemma.options), 2)
        chosen_entry = lore.apply_wild_choice(scenario.game, dilemma.options[0])
        self.assertIsNotNone(chosen_entry)

    def test_crusade_progression_and_boons(self) -> None:
        rng = random.Random(99)
        crusade = lore.create_crusade(elephant=False)
        self.assertEqual(len(crusade.roster), 16)
        scenario, diff = lore.create_crusade_stage(crusade, rng=rng)
        self.assertEqual(diff, "Escudero")
        self.assertTrue(scenario.game.legal_moves(WHITE))
        note = lore.apply_crusade_boon(crusade, "veteran", rng=rng)
        self.assertIn("Veterano", note)
        self.assertEqual(sum(1 for p in crusade.roster if p.veteran), 2)

    def test_narrative_entries(self) -> None:
        game = lore.create_game(elephant=True)
        moves = game.legal_moves_from(7, 2)
        move = game.apply_move(moves[0])
        entry = lore.narrate_move(move, game, check=False, mate=False, chapter=1)
        self.assertEqual(entry.tag, "move")
        fog = lore.fog_entry(1)
        self.assertEqual(fog.tag, "fog")

    def test_four_kingdoms_and_multi_front_war(self) -> None:
        # 1. Partida clásica con los nuevos reinos (Forja Carmesí vs Pacto de la Espesura) y Elefante (20 + 2 saltos = 22)
        game_rg = lore.create_game(elephant=True, player_color=RED, enemy_color=GREEN)
        self.assertEqual(game_rg.turn_order, [RED, GREEN])
        self.assertEqual(len(game_rg.legal_moves(RED)), 22)
        self.assertEqual(len(game_rg.legal_moves(GREEN)), 22)
        self.assertEqual(game_rg.piece_at(7, 4).name, "Rey Leónidas")
        self.assertEqual(game_rg.piece_at(7, 3).name, "Reina Gorgo")
        self.assertEqual(game_rg.piece_at(0, 4).name, "Rey Vercingétorix")
        self.assertEqual(game_rg.piece_at(0, 3).name, "Reina Boudica")
        for c in ALL_COLORS:
            self.assertIn("culture", lore.FACTIONS[c])
            self.assertIn("sovereigns", lore.FACTIONS[c])
            self.assertIn("lore", lore.FACTIONS[c])

        # 2. Cruzada encadenada con otro reino y rotación de los 3 reinos rivales
        crusade = lore.create_crusade(elephant=False, player_color=RED)
        self.assertEqual(crusade.player_color, RED)
        self.assertEqual(len(crusade.stage_rivals), 4)
        self.assertEqual(set(crusade.stage_rivals), {WHITE, BLACK, GREEN})

        # 3. Guerra de los Cuatro Frentes simultánea
        four_game = lore.create_four_fronts_game(elephant=True, player_color=WHITE)
        self.assertEqual(len(four_game.turn_order), 4)
        self.assertEqual(set(four_game.turn_order), set(ALL_COLORS))
        for color in ALL_COLORS:
            self.assertIsNotNone(four_game.find_king(color))
            self.assertGreater(len(four_game.legal_moves(color)), 0)

        # IA encuentra jugada válida en Guerra de 4 Frentes
        ai_move = find_best_move(four_game, depth=1, randomness=0.0, time_limit=0.5, rng=random.Random(7))
        self.assertIsNotNone(ai_move)

    def test_imperial_12x12_and_mythic_boon(self) -> None:
        imp_game = lore.create_imperial_game(player_color=WHITE, enemy_color=BLACK)
        self.assertEqual(imp_game.size, 12)
        kinds_present = {
            p.kind for row in imp_game.grid for p in row if p is not None
        }
        for fk in FAIRY_KINDS:
            self.assertIn(fk, kinds_present)
        self.assertGreater(len(imp_game.legal_moves(WHITE)), 40)
        self.assertGreater(len(imp_game.legal_moves(BLACK)), 40)

        ai_imp = find_best_move(imp_game, depth=1, randomness=0.0, time_limit=0.6, rng=random.Random(11))
        self.assertIsNotNone(ai_imp)
        assert ai_imp is not None
        self.assertTrue(len(move_notation(ai_imp, size=12)) >= 2)

        crusade = lore.create_crusade(elephant=False)
        mythic_note = lore.apply_crusade_boon(crusade, "mythic", rng=random.Random(21))
        self.assertTrue(any(p.kind in FAIRY_KINDS for p in crusade.roster))
        self.assertTrue(len(mythic_note) > 10)


if __name__ == "__main__":
    unittest.main()
