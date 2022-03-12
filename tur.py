# eg4-montyhall.py
import random
def run_trial(switch_doors, ndoors=3):
    """
    Run a single trial of the Monty Hall problem, with or without switching
    after the game show host reveals a goat behind one of the unchosen doors.
    (switch_doors is True or False). The car is behind door number 1 and the
    game show host knows that. Returns True for a win, otherwise returns False.
    """
    # """
    # Запуск одиночного испытания парадокса (задачи) Монти Холла с изменением или без
    # изменения варианта выбора, после того как ведущий предъявил козу, открыв одну из
    # невыбранных дверей. (Смена выбора двери обозначена как True или False.) Автомобиль
    # находится за дверью номер 1, и ведущий знает это. При выигрыше возвращается значение
    # True, иначе возвращается False.
    # """
    # Выбор случайной двери из доступных ndoors.
    chosen_door = random.randint(1, ndoors)
    if switch_doors:
        # Обнаружена коза.
        revealed_door = 3 if chosen_door==2 else 2
        # Изменение варианта выбора на любую другую дверь, отличную от выбранной
        # изначально, при одной открытой двери, за которой обнаружилась коза.
        available_doors = [dnum for dnum in range(1, ndoors+1)
        if dnum not in (chosen_door, revealed_door)]
        chosen_door = random.choice(available_doors)
    # Выигрыш, если выбрана дверь номер 1.
    return chosen_door == 1 		
def run_trials(ntrials , switch_doors , ndoors=3):
    """
    Run ntrials iterations of the Monty Hall problem with ndoors doors, with
    and without switching (switch_doors = True or False). Returns the number
    of trials which resulted in winning the car by picking door number 1.
    """
    # """
    # Запуск ntrials итераций задачи Монти Холла с ndoors дверьми с изменением или без
    # изменения варианта выбора (switch_doors = True или False). Возвращает количество
    # испытаний, завершившихся выигрышем автомобиля при выборе двери номер 1.
    # """
    nwins = 0
    for i in range(ntrials):
        if run_trial(switch_doors, ndoors):
            nwins += 1
    return nwins
ndoors, ntrials = 3, 10000
nwins_without_switch = run_trials(ntrials, False, ndoors)
nwins_with_switch = run_trials(ntrials, True, ndoors)
print('Monty Hall Problem with {} doors'.format(ndoors))
print('Proportion of wins without switching: {:.4f}'.format(nwins_without_switch/ntrials))
print('Proportion of wins with switching: {:.4f}'.format(nwins_with_switch/ntrials))