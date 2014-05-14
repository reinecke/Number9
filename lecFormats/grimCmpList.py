#!/usr/bin/env python
cmpMap = {
"above_door.3do":"above_door.cmp",
"ac_belts.3do":"coralmin.cmp",
"action_hand.3do":"action.cmp",
"action_manny.3do":"action.cmp",
"activate_baster.3do":"baster.cmp",
"activate_chisel.3do":"mile8.cmp",
"activate_cigcase.3do":"mile5.cmp",
"activate_coral.3do":"item.cmp",
"activate_detector.3do":"carla.cmp",
"activate_dogtags.3do":"dogtag.cmp",
"activate_grinder.3do":"bone_grind.cmp",
"activate_gun.3do":"mile8.cmp",
"activate_hand.3do":"m_chow.cmp",
"activate_hand.3do":"siberian.cmp",
"activate_key.3do":"mile5.cmp",
"activate_mouthpiece.3do":"item.cmp",
"activate_mt_balloon.3do":"item.cmp",
"activate_nitro.3do":"nitro.cmp",
"activate_opener.3do":"can_opener.cmp",
"activate_photo.3do":"celso.cmp",
"activate_rag.3do":"rag.cmp",
"activate_ragoil.3do":"rag.cmp",
"activate_salnotes.3do":"cafe.cmp",
"activate_salnotes.3do":"mile5.cmp",
"activate_salnotes.3do":"sal_note.cmp",
"activate_spcan.3do":"sprout_can.cmp",
"activate_tix_machine.3do":"tix_printer.cmp",
"activate_ve_bottle.3do":"ve_bottle.cmp",
"aitor.3do":"aitor.cmp",
"albinozod.3do":"alb.cmp",
"anchor.3do":"mile8.cmp",
"anchor_note2.3do":"anchornote.cmp",
"anchor_note.3do":"anchornote.cmp",
"ashtray.3do":"mile9.cmp",
"axe.3do":"mile9.cmp",
"bag_object_anim.3do":"domino.cmp",
"balloon_cat.3do":"items_more.cmp",
"balloon_left_fill_1st.3do":"items_3.cmp",
"balloon_left_fill_2nd.3do":"items_3.cmp",
"balloon_man.3do":"ballman.cmp",
"balloon_to_stuff2.3do":"balloon2.cmp",
"balloon_to_stuff.3do":"items_3.cmp",
"bar1.3do":"chepito.cmp",
"bar2.3do":"chepito.cmp",
"baster.3do":"baster.cmp",
"bcp1.3do":"bcp1.cmp",
"bcp1_head1.3do":"bcp1.cmp",
"bcp1_head2.3do":"bcp1.cmp",
"bcp2.3do":"slisko.cmp",
"bcp2_head1.3do":"slisko.cmp",
"bcp2_head2.3do":"slisko.cmp",
"bcp4.3do":"gunar.cmp",
"bcp4_head1.3do":"gunar.cmp",
"bcp4_head2.3do":"gunar.cmp",
"bcp5.3do":"bcp5.cmp",
"bcp7.3do":"bcp7.cmp",
"beaver.3do":"beaver.cmp",
"beaver_fire.3do":"beaver.cmp",
"beaver_fire_head.3do":"beaver.cmp",
"beaver_frozen.3do":"beaver.cmp",
"bee.3do":"seabees.cmp",
"belch.3do":"items_3.cmp",
"betting_stub.3do":"betting_stub.cmp",
"bibi.3do":"ang.cmp",
"bi_head1.3do":"ang.cmp",
"bi_head2.3do":"ang.cmp",
"bi_head3.3do":"ang.cmp",
"binder.3do":"cafe.cmp",
"bondo_mp.3do":"domino.cmp",
"bone.3do":"suit.cmp",
"bone_big.3do":"action.cmp",
"bone_big.3do":"suit.cmp",
"bonewagon.3do":"bonewagon.cmp",
"bowl.3do":"bc_stuff.cmp",
"bowlsley.3do":"bowlsley.cmp",
"bread.3do":"item.cmp",
"bread_model.3do":"items_more.cmp",
"brennis.3do":"brennis.cmp",
"brennis_arm.3do":"brennis.cmp",
"br_fire.3do":"beaver.cmp",
"br_head2.3do":"brennis.cmp",
"br_head3.3do":"brennis.cmp",
"bruno_pjs.3do":"bruno.cmp",
"bruno_skel.3do":"bruno.cmp",
"bs_head1.3do":"bowlsley.cmp",
"bs_head2.3do":"bowlsley.cmp",
"bs_head3.3do":"bowlsley.cmp",
"bv_key.3do":"bv_key.cmp",
"caneman.3do":"nc_crowd.cmp",
"canister.3do":"item.cmp",
"can_note.3do":"item.cmp",
"can_opener.3do":"can_opener.cmp",
"card.3do":"item.cmp",
"cards.3do":"item.cmp",
"carla.3do":"carla.cmp",
"cask.3do":"cask_wine.cmp",
"cask_half.3do":"cask_wine.cmp",
"cc_card.3do":"mile5_more.cmp",
"cc_gun.3do":"mile8.cmp",
"cc_pass.3do":"mile5.cmp",
"cc_tix_printer.3do":"tix_printer.cmp",
"cc_toga.3do":"charlie.cmp",
"ce_head1.3do":"celso.cmp",
"ce_head2.3do":"celso.cmp",
"ce_head3.3do":"celso.cmp",
"celso.3do":"celso.cmp",
"celso_fancy.3do":"celso.cmp",
"ce_swankhd1.3do":"celso.cmp",
"ce_swankhd2.3do":"celso.cmp",
"ce_swankhd3.3do":"celso.cmp",
"chain.3do":"siberian.cmp",
"charlie.3do":"charlie.cmp",
"chepito.3do":"chepito.cmp",
"chief_bogan.3do":"bogen.cmp",
"chisel_inv.3do":"mile8.cmp",
"cigar.3do":"max.cmp",
"cigarette.3do":"item.cmp",
"cigcase.3do":"mile5.cmp",
"coat.3do":"coat.cmp",
"coffee_long.3do":"coffee.cmp",
"coffee_medium.3do":"coffee.cmp",
"coffee_pot.3do":"thunder.cmp",
"coffee_short.3do":"coffee.cmp",
"coffinshooter.3do":"bc_stuff.cmp",
"co_head.3do":"copal.cmp",
"coin_pile.3do":"roulette.cmp",
"comm_book.3do":"comm_book.cmp",
"comm_book.3do":"mile5.cmp",
"comm_book_inv.3do":"comm_book.cmp",
"coral2.3do":"item.cmp",
"coral.3do":"item.cmp",
"coral_miner.3do":"coralmin.cmp",
"coral_rope.3do":"item.cmp",
"coral_scrap.3do":"item.cmp",
"crane.3do":"crane.cmp",
"crane_scoop.3do":"crane.cmp",
"crumb_model.3do":"item.cmp",
"crumb_pile.3do":"item.cmp",
"ct_gun.3do":"mile8.cmp",
"ct_head2.3do":"chepito.cmp",
"ct_head3.3do":"chepito.cmp",
"cup_bottle.3do":"do_items.cmp",
"cy_belts.3do":"coralmin.cmp",
"deck_o_cards.3do":"item.cmp",
"deflated_balloon.3do":"item.cmp",
"dg_head2.3do":"doug.cmp",
"dg_head3.3do":"doug.cmp",
"dingo_balloon.3do":"items_more.cmp",
"dingo_inv.3do":"items_more.cmp",
"dog_tag_inv.3do":"dogtag.cmp",
"dogtags.3do":"dogtag.cmp",
"do_head2.3do":"domino.cmp",
"do_head3.3do":"domino.cmp",
"domino_boxing.3do":"domino.cmp",
"domino_isle.3do":"domino.cmp",
"doug.3do":"doug.cmp",
"eggs.3do":"item.cmp",
"ehand.3do":"item.cmp",
"ei_outside.3do":"ei_outside.cmp",
"elev_shaft.3do":"elev_shaft.cmp",
"empty_balloon_hold.3do":"items_3.cmp",
"empty_balloon_inv.3do":"items_3.cmp",
"eva_rev.3do":"eva_sv.cmp",
"eva_sec.3do":"eva_sv.cmp",
"ext_chem.3do":"items_3.cmp",
"ext_object.3do":"items_3.cmp",
"fatlady.3do":"nc_crowd.cmp",
"filled_balloon.3do":"balloon2.cmp",
"filled_balloon.3do":"items_3.cmp",
"finish_photo.3do":"photofinish.cmp",
"fire_extinguisher.3do":"items_3.cmp",
"fire_ext_inv.3do":"items_3.cmp",
"fishout_key.3do":"mile5.cmp",
"flakes.3do":"bone_flakes.cmp",
"flower_trail.3do":"bone_flakes.cmp",
"foam_mug.3do":"foam_mug.cmp",
"folded_coat.3do":"coat.cmp",
"forklift.3do":"forklift.cmp",
"fridge_door.3do":"fridge.cmp",
"full_baster.3do":"baster.cmp",
"gatekeeper.3do":"gatekeep.cmp",
"gk_head2.3do":"gatekeep.cmp",
"gk_head3.3do":"gatekeep.cmp",
"gk_note.3do":"gatekeep.cmp",
"glass.3do":"raoul.cmp",
"gl_head1.3do":"glottis.cmp",
"gl_head2.3do":"glottis.cmp",
"gl_head3.3do":"glottis.cmp",
"gl_head4.3do":"glottis.cmp",
"gl_head5.3do":"glottis.cmp",
"gl_heart.3do":"glottis.cmp",
"gl_heart_beat.3do":"glottis.cmp",
"glottis.3do":"glottis.cmp",
"glottis_sailor.3do":"glottis.cmp",
"glottis_tux.3do":"glottis.cmp",
"gl_peek.3do":"glottis.cmp",
"gl_small_heart.3do":"glottis.cmp",
"gold_bottle.3do":"mile5.cmp",
"gold_flake_inv.3do":"mile5.cmp",
"grinder_inv.3do":"bone_grind.cmp",
"gun.3do":"bowlsley.cmp",
"gun.3do":"mile8.cmp",
"hammer.3do":"ang.cmp",
"hammer.3do":"mile8.cmp",
"hand.3do":"cafe.cmp",
"hand_grinder.3do":"bone_grind.cmp",
"hand_inv.3do":"bone_grind.cmp",
"headphones.3do":"domino.cmp",
"hector2.3do":"hector.cmp",
"he_head1.3do":"hector.cmp",
"he_head2.3do":"hector.cmp",
"he_head3.3do":"hector.cmp",
"he_head4.3do":"hector.cmp",
"he_head5.3do":"hector.cmp",
"hitman1.3do":"hitmen.cmp",
"hitman2.3do":"hitmen.cmp",
"hitman3.3do":"hitmen.cmp",
"hka_pipe_start.3do":"hooka.cmp",
"hooka.3do":"hooka.cmp",
"hooka_base.3do":"hooka.cmp",
"hooka_pipe.3do":"hooka.cmp",
"hooka_water.3do":"hooka.cmp",
"hr_pass.3do":"mile5.cmp",
"hr_pass.3do":"mile5_more.cmp",
"inflated_balloon.3do":"item.cmp",
"inflated_balloon.3do":"items_more.cmp",
"inv_tix_machine.3do":"tix_printer.cmp",
"it_head2.3do":"aitor.cmp",
"it_head3.3do":"aitor.cmp",
"jello_object.3do":"hooka.cmp",
"key_basket.3do":"carla.cmp",
"lengua2.3do":"mile5_more.cmp",
"lengua2.3do":"ticket.cmp",
"lengua.3do":"mile5_more.cmp",
"lever.3do":"forklift.cmp",
"levers.3do":"nautical.cmp",
"life_mug.3do":"bruno.cmp",
"life_mug.3do":"foam_mug.cmp",
"liquid_nitro.3do":"nitro.cmp",
"logbook.3do":"log_book.cmp",
"logbook_inv.3do":"log_book.cmp",
"lola.3do":"lola.cmp",
"lsa_photo.3do":"lsa_photo.cmp",
"lupe.3do":"lupe.cmp",
"ma_action_ma.3do":"action.cmp",
"ma_cigcase.3do":"mile5.cmp",
"ma_climb_suit.3do":"suit.cmp",
"manny_cafe.3do":"cafe.cmp",
"manny_chow.3do":"m_chow.cmp",
"manny_chowthund.3do":"charlie.cmp",
"manny_chowthund.3do":"m_chow.cmp",
"manny_chowthund.3do":"siberian.cmp",
"manny_deathrobe.3do":"suit.cmp",
"manny_head2.3do":"suit.cmp",
"manny_head3.3do":"nautical.cmp",
"manny_naut2.3do":"nautical.cmp",
"manny_naut.3do":"nautical.cmp",
"manny_siberian.3do":"siberian.cmp",
"manny_sibthund.3do":"siberian.cmp",
"mannysuit.3do":"suit.cmp",
"maximino_3do.3do":"max.cmp",
"mcc_ehand.3do":"m_chow.cmp",
"mc_ehand.3do":"cafe.cmp",
"md_ehand.3do":"md_inv.cmp",
"md_flower.3do":"md_flower.cmp",
"md_sync_ol_skrts.3do":"suit.cmp",
"meche.3do":"meche.cmp",
"meche_island2.3do":"meche.cmp",
"meche_island.3do":"meche.cmp",
"meche_ruba.3do":"meche.cmp",
"meche_snow.3do":"meche_snow.cmp",
"membrillo2.3do":"membrill.cmp",
"mem_head1.3do":"membrill.cmp",
"mem_head2.3do":"membrill.cmp",
"mem_head3.3do":"membrill.cmp",
"memtool.3do":"mile8.cmp",
"me_seduce_sheet.3do":"charlie.cmp",
"metal_detector.3do":"carla.cmp",
"mi_cigg.3do":"mile9.cmp",
"mi_paper.3do":"mile9.cmp",
"m_mechanic.3do":"glottis.cmp",
"m_mechanic.3do":"mechanic.cmp",
"mm_extinguisher.3do":"items_3.cmp",
"mm_head2.3do":"glottis.cmp",
"mm_head3.3do":"glottis.cmp",
"mm_wrench.3do":"glottis.cmp",
"mn_hand.3do":"nautical.cmp",
"mop.3do":"celso.cmp",
"mp_big.3do":"domino.cmp",
"mrs_flores.3do":"celso.cmp",
"msb_hand.3do":"siberian.cmp",
"msb_hold_sheet.3do":"charlie.cmp",
"msb_inv_gun.3do":"msb_inv.cmp",
"mth_head1.3do":"thunder.cmp",
"mth_head2.3do":"thunder.cmp",
"mth_head3.3do":"thunder.cmp",
"mug2_master2.3do":"black.cmp",
"mug_fire.3do":"mug_fire.cmp",
"mug_rack.3do":"mile9.cmp",
"mx_head1.3do":"max.cmp",
"mx_head2.3do":"max.cmp",
"mx_head3.3do":"max.cmp",
"naranja.3do":"naranja.cmp",
"new_nylons.3do":"mile8.cmp",
"nick.3do":"nick.cmp",
"nitro.3do":"nitro.cmp",
"nitro_inv.3do":"nitro.cmp",
"nk_head2.3do":"nick.cmp",
"nk_head3.3do":"nick.cmp",
"n_l_photo.3do":"mile5_more.cmp",
"note.3do":"item.cmp",
"nr_bottle.3do":"items_3.cmp",
"nv_paper.3do":"nick.cmp",
"octo_eye.3do":"octo_eye.cmp",
"ol_flowers.3do":"flowers_face.cmp",
"ol_gun.3do":"hitmen.cmp",
"ol_gun.3do":"mile8.cmp",
"olive_can.3do":"action.cmp",
"olivia.3do":"olivia.cmp",
"olivia_big.3do":"olivia.cmp",
"open_suitcase.3do":"suitcase.cmp",
"p80_01a_gun.3do":"mile8.cmp",
"passoutgirl.3do":"bcp5.cmp",
"phone2.3do":"cafe.cmp",
"photopass_env.3do":"cafe.cmp",
"pickaxe.3do":"mile8.cmp",
"power_chisel.3do":"mile8.cmp",
"pugsly.3do":"ang.cmp",
"pu_head1.3do":"ang.cmp",
"pu_head2.3do":"ang.cmp",
"pu_head3.3do":"ang.cmp",
"pump_action.3do":"bonewagon.cmp",
"pump_tree.3do":"tr_scene.cmp",
"puncher.3do":"item.cmp",
"ra_2head1.3do":"raoul.cmp",
"ra_2head2.3do":"raoul.cmp",
"ra_2head3.3do":"raoul.cmp",
"rag_inv.3do":"msb_inv.cmp",
"ra_head1.3do":"raoul.cmp",
"ra_head2.3do":"raoul.cmp",
"ra_head3.3do":"raoul.cmp",
"raoul.3do":"raoul.cmp",
"Raoul_w_tray.3do":"raoul.cmp",
"Raul_waiter-raoul.3do":"raoul.cmp",
"remote.3do":"cafe.cmp",
"rfrost_balloon.3do":"items_more.cmp",
"rfrost_gripped.3do":"items_more.cmp",
"rope.3do":"yr1_pal1.cmp",
"rope_ledge.3do":"yr1_pal1.cmp",
"rope_new2.3do":"yr1_pal1.cmp",
"roulette.3do":"roulette.cmp",
"rt_handle.3do":"roulette.cmp",
"rt_wheel.3do":"roulette.cmp",
"sal_dead.3do":"eva_sv.cmp",
"sals_eggs.3do":"item.cmp",
"sal_spit.3do":"flowers_face.cmp",
"salvador.3do":"eva_sv.cmp",
"scythe_do_fight.3do":"items_more.cmp",
"scythe_door.3do":"items_more.cmp",
"scythe_fight.3do":"items_more.cmp",
"scythe_folded.3do":"items_more.cmp",
"scythe_lock.3do":"items_more.cmp",
"scythe_long.3do":"items_more.cmp",
"scythe_pull.3do":"items_more.cmp",
"scythe_putaway.3do":"items_more.cmp",
"scythe_putback_md.3do":"items_more.cmp",
"scythe_short.3do":"items_more.cmp",
"scythe_shorting.3do":"items_more.cmp",
"scythe_sprinkle.3do":"items_more.cmp",
"scythe_takeout.3do":"items_more.cmp",
"scythe_takeout_long.3do":"items_more.cmp",
"severed_sal.3do":"eva_sv.cmp",
"shipbottle.3do":"ve_bottle.cmp",
"shooters2.3do":"bc_stuff.cmp",
"shooters.3do":"bc_stuff.cmp",
"shooters_start.3do":"bc_stuff.cmp",
"signpost.3do":"signpost.cmp",
"signpost_adjust.3do":"signpost.cmp",
"signpost_lit.3do":"signpost.cmp",
"sn_head2.3do":"nc_crowd.cmp",
"sn_head3.3do":"nc_crowd.cmp",
"spider.3do":"spider.cmp",
"spinner.3do":"nc_crowd.cmp",
"sprout_can.3do":"sprout_can.cmp",
"sprout_can_inv.3do":"msb_inv.cmp",
"stick.3do":"item.cmp",
"stick.3do":"items_more.cmp",
"stocking.3do":"mile8.cmp",
"suitcase.3do":"suitcase.cmp",
"sv_deadhd1.3do":"eva_sv.cmp",
"sv_deadhd2.3do":"eva_sv.cmp",
"sv_deadhd3.3do":"eva_sv.cmp",
"sv_large_head.3do":"eva_sv.cmp",
"sv_medium_head.3do":"eva_sv.cmp",
"sv_small_head.3do":"eva_sv.cmp",
"tboy1.3do":"thunder.cmp",
"tboy2.3do":"thunder.cmp",
"thb_mug.3do":"thunder.cmp",
"th_snow.3do":"bone_flakes.cmp",
"tinykey.3do":"mile5.cmp",
"tix_3do.3do":"ticket.cmp",
"tix_flop.3do":"ticket.cmp",
"tix_only.3do":"ticket.cmp",
"toaster_fire.3do":"beaver.cmp",
"toto.3do":"toto.cmp",
"toto_drill.3do":"mile8.cmp",
"toto_drop_na.3do":"toto.cmp",
"tp_hand.3do":"cafe.cmp",
"tray1.3do":"bc_stuff.cmp",
"tray2.3do":"bc_stuff.cmp",
"tumbler.3do":"mile9.cmp",
"turbanman.3do":"nc_crowd.cmp",
"twist_balloon.3do":"items_more.cmp",
"unicycle_man.3do":"uni_man.cmp",
"uni_hat.3do":"uni_man.cmp",
"uni_head2.3do":"uni_man.cmp",
"uni_head3.3do":"uni_man.cmp",
"union_card.3do":"mile5_more.cmp",
"vault_wheel.3do":"mile9.cmp",
"ve_bottle.3do":"ve_bottle.cmp",
"velasco.3do":"velasco.cmp",
"v_head1.3do":"velasco.cmp",
"v_head2.3do":"velasco.cmp",
"v_head3.3do":"velasco.cmp",
"waiter.3do":"waiter.cmp",
"waiter_head1.3do":"waiter.cmp",
"waiter_head2.3do":"waiter.cmp",
"weight.3do":"tr_scene.cmp",
"wheelbarrow.3do":"tr_scene.cmp",
"wine_end.3do":"cask_wine.cmp",
"winespill.3do":"cask_wine.cmp",
"wine_stream.3do":"cask_wine.cmp",
"wkorderinv.3do":"item.cmp",
"workorder.3do":"item.cmp",
"xbrdg.3do":"forklift.cmp",
}
