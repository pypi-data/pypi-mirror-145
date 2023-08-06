def main():	
    
    import os
    import numpy as np

    ### SYSTEM SPECIFIC ###

    ps_dir = os.path.dirname(__file__)+"./pseudos/"  # Directory in which PBE_ONCV, PBESOL_ONCV, LDA_ONCV dirs are present

    parallel = 'mpirun'
    b = sorted(os.environ["PATH"].split(":"))
    for i in b:
        if "aprun" in os.listdir(i):
            parallel = 'aprun'
            break

    ncores = int(np.ceil(os.cpu_count()/2+0.1)) # default

    ### DO NOT CHANGE BELOW UNLESS NEEDED ###


    from ase import atom
    from ase.dft.kpoints import bandpath
    from ase.io import read, write
    from ase.calculators.espresso import Espresso
    import argparse
    import matplotlib.pyplot as plt

    def load_data(filename, head=0):
        import numpy as np
        f = open(filename, 'r')
        lines = [i.split() for i in f.readlines()[head:]]
        f.close()

        for n, i in enumerate(lines):
            for o, j in enumerate(i):
                try:
                    lines[n][o] = float(j)
                except:
                    try:
                        lines[n][o] = eval(j)
                    except:
                        lines[n][o] = j

        length = max(map(len, lines))
        y=np.array([xi+[None]*(length-len(xi)) for xi in lines])

        return y

    def get_pressure(file):
        f = open(file)
        lines = f.readlines()
        f.close()

        os.system(f'tac {file} > cv')
        p = float(os.popen("grep -m1 kbar cv").read().split(' ')[-1][0:-1])
        os.system('rm cv')
        return p

    def get_kpts(file='mesh_k'):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        kpts = []
        for i in lines[1:]:
            j = i.split()[1:4]
            k = [float(l) for l in j]
            kpts.append(k)

        return kpts

    def dict_to_string(inp_dict):
        line = ''
        for i in inp_dict:
            b = inp_dict[i]
            if type(b)==str:
                try:
                    val = int(b)
                except:
                    try:
                        val = float(b)
                    except:
                        if b.lower() == '.true.' or b.lower()=='.false.':
                            val = b
                        else:
                            val = f"'{b}'"
            elif type(b) == list:
                val = ''
                for item in b:
                    val += f'{float(item)} '
            else:
                val = b

            a = f'{i} = {val} \n'
            line += a
        return line


    pwd = os.getcwd()
    parse = argparse.ArgumentParser()
    parse.add_argument('-f', '--file', help='Give structure file', type=str,
                        default=f'POSCAR')
    parse.add_argument('-ppd', '--pseudo_dir', help='Pseudo potential (names should be like C.UPF) directroy, you can select pbe, pbesol and lda', type=str, default='pbe')
    parse.add_argument('-c', '--calc', help='Type of calculation', type=str, default='scf', choices=['encut', 'kgrid', 'vacuum', 'vc-relax', 'scf', 'nscf', 'bands','dos', 'pressure', 'eos', 'harmonic', 'ph_pre', 'ph_mid', 'ph_post', 'ph_bands', 'ph_dos', 'epw_pre', 'epw_post'])
    parse.add_argument('-vdr', '--vac_dir', help='Vacuum direction', type=int, default=None, choices=[1,2,3])
    parse.add_argument('-e', '--encut', help='ENCUT', type=float, default=50)
    parse.add_argument('-k', '--kgrid', help='KGRID', type=int,nargs=3, default=[4,4,4])
    parse.add_argument('-v', '--vacuum', help='VACUUM', type=float, default=10.0)
    parse.add_argument('-t', '--threshold', help='Threshold', type=float, default=0.01)
    parse.add_argument('-rp', '--required_pressure', help='Required pressure in kbar', type=float, default=100)
    parse.add_argument('-ic', '--initial_compression', help='Initial compression faction', type=float, default=0.9)
    parse.add_argument('-bp', '--band_path', help='Bandpath', default=None, type=str)
    parse.add_argument('-ns', '--nofstructures', help='Number of structures for EoS fitting', default=10, type=str)
    parse.add_argument('-aid', "--atom_id", help="Id 0f atom to move for harmonic calc, starting from 0.", default=None, type=int)
    parse.add_argument('-dd', "--disp_dir", help="Direction in which displacement should be, x=0, y=1, z=2", default=None, type=int, choices=[0,1,2])
    parse.add_argument('-emin', '--enmin_for_bands', default=None, type=float)
    parse.add_argument('-emax', '--enmax_for_bands', default=None, type=float)
    parse.add_argument('-par', '--pars_file', default=None, type=str)
    parse.add_argument('-ppn', '--nprocs', default=ncores, type=int)
    parse.add_argument('-nq', '--nqpts', default=None, type=int)
    parse.add_argument('-asr', '--asr', help = 'Acoustic sum rule', default='simple')
    parse.add_argument('-npool', '--npool', help = 'NPOOL for PW.X and EPW.X', default=None, type=int)
    args = vars(parse.parse_args())

    structure = args['file']
    ppd = args['pseudo_dir']
    calc_type = args['calc']
    vac_dir = args['vac_dir']
    encut = args['encut']
    kgrid = [args['kgrid'][0], args['kgrid'][1],args['kgrid'][2] ]
    vacuum = args['vacuum']
    threshold = args['threshold']
    rp = args['required_pressure']
    ic = args['initial_compression']
    band_path = args['band_path']
    ns = args['nofstructures']
    aid = args['atom_id']
    dd = args['disp_dir']
    emin = args['enmin_for_bands']
    emax = args['enmax_for_bands']
    par = args['pars_file']
    ppn = args['nprocs']
    nq = args['nqpts']
    asr = args['asr']
    npool = args['npool']

    if par is not None:
        par_dict = {}
        parf = open(par, 'r')
        for line in parf:
            st = line.split()
            if len(st) > 2:
                key = st[0]
                value = st[1:]
            else:
                key, value = st
            try:
                par_dict[key] = int(value)
            except:
                try:
                    par_dict[key] = float(value)
                except:
                    par_dict[key] = value


    if npool is None:
      os.environ["ASE_ESPRESSO_COMMAND"] = f'{parallel} -n {ppn} pw.x -in espresso.pwi | tee espresso.pwo'
    else:
      os.environ["ASE_ESPRESSO_COMMAND"] = f'{parallel} -n {ppn} pw.x -npool {npool} -in espresso.pwi | tee espresso.pwo'


    atoms = read(structure)

    types = list(set(atoms.get_chemical_symbols()))

    prefix = atoms.get_chemical_formula()
    input_data  ={
        'ecutwfc' : encut,
        'occupations' : 'smearing',
        'smearing' : 'gaussian',
        'degauss' : 0.05,
        'prefix' : prefix
    }

    pseudos = {}
    for i in types:
        if ppd=='pbe':
            input_data['pseudo_dir'] = ps_dir + '/PBE_ONCV/'
            pseudos[i] = i+'.UPF'
        elif ppd=='pbesol':
            input_data['pseudo_dir'] = ps_dir + '/PBESOL_ONCV/'
            pseudos[i] = i+'.UPF'
        elif ppd=='lda':
            input_data['pseudo_dir'] = ps_dir + '/LDA_ONCV/'
            pseudos[i] = i+'.UPF'
        else:   
            input_data['pseudo_dir'] = os.path.abspath(ppd)+'/'    
            pseudos[i] = i+'.UPF'



    ph_data = {
      'tr2_ph':'1e-12',
      'alpha_mix(1)':0.1,
      'ldisp':'.true.',
      'search_sym':'.false.',
      'trans':'.true.',
      'recover':'.true.',
      'start_q':1,
      'last_q':1,
      'nq1':kgrid[0],
      'nq2':kgrid[1],
      'nq3':kgrid[2],
      'prefix':prefix,
      'fildyn':f'{prefix}.dyn_q',
      'fildvscf':f'dvscf_q',
      'outdir':f'{pwd}/scf/'
    }

    epw_data = {
        'prefix':prefix,
        'outdir':f'{pwd}/scf/',
        'asr_typ':asr,
        'dvscf_dir':f'{pwd}/epw/save',
        'eliashberg':'.true.',
        'elph':'.true.',
        'fsthick':0.5,
        'kmaps':'.false.',
        'epbwrite':'.true.',
        'wannierize':'.true.',
        'proj(1)':'random',
        'ephwrite':'.true.',
        'iverbosity':2,
        'laniso':'.true.',
        'limag':'.true.',
        'lpade':'.true.',
        'nstemp':1,
        'temps':4,
        'muc':0.16,
        'nk1':kgrid[0],
        'nk2':kgrid[1],
        'nk3':kgrid[2],
        'nq1':kgrid[0],
        'nq2':kgrid[1],
        'nq3':kgrid[2],
        'mp_mesh_k':'.true.',
        'nkf1':20,
        'nkf2':20,
        'nkf3':20,
        'nqf1':20,
        'nqf2':20,
        'nqf3':20
    }

    dos_data = {
      'prefix':prefix,
      'outdir':f'{pwd}/scf/',
      'DeltaE':0.01
    }

    if par is not None:
        input_data.update(par_dict)
        ph_data.update(par_dict)
        epw_data.update(par_dict)
        dos_data.update(par_dict)

    kpts = kgrid
    if vac_dir is not None:
        kpts[vac_dir-1] = 1

    calc = Espresso(pseudopotentials = pseudos,
                    tprnfor=True,
                    tstress=True,
                    kpts=kpts,
                    input_data=input_data
                    )

    if calc_type=='encut':    
        energies = []
        encuts = []
        i = 30
        converged = False
        while not converged:
            atoms.translate([0,0,0.01])
            dd = f'{pwd}/encut/{i}'
            #input_data['ecutwfc'] = i
            #input_data['outdir'] = dd
            input_data.update({'ecutwfc' : i,
                               'outdir'  : dd})
            calc.set(input_data = input_data, kpts=kpts)
            atoms.calc = calc
            os.system(f'mkdir -p {pwd}/encut/{i}')
            
            os.chdir(dd)
            print('###########', i)
            e = atoms.get_potential_energy()
            energies.append(e)
            encuts.append(i)
            if len(energies) > 2 and abs(energies[-1]-energies[-2]) < threshold and abs(energies[-3]-energies[-2]) < threshold:
                converged = True
            else:
                i+=10
            os.chdir(pwd)
        f = open('encut_conv', 'a')
        for i in range(len(encuts)):
            st = f'{encuts[i]}   {energies[i]}\n'
            f.write(st)
        f.close()

    if calc_type=='kgrid':
        input_data['calculation'] = 'scf'
        energies = []
        kgrids = []
        converged = False
        kpts = np.array([2, 2, 2])
        while not converged:
            if vac_dir is not None:
                kpts[vac_dir-1] = 1
            print('######', kpts)
            input_data['outdir'] = f'{pwd}/kgrid/{np.max(kpts)}'
            calc.set(input_data = input_data, kpts=kpts.tolist())
            atoms.calc = calc
            os.system(f'mkdir -p {pwd}/kgrid/{np.max(kpts)}')
            os.chdir(f'{pwd}/kgrid/{np.max(kpts)}')
            e = atoms.get_potential_energy()
            energies.append(e)
            kgrids.append(np.max(kpts))
            if len(energies) > 2 and abs(energies[-1]-energies[-2]) < threshold and abs(energies[-3]-energies[-2]) < threshold:
                converged = True
            else:
                kpts = kpts + np.array([2, 2, 2])
        os.chdir(pwd)
        f = open('kgrid_conv', 'a')
        for i in range(len(kgrids)):
            st = f'{kgrids[i]}   {energies[i]}\n'
            f.write(st)
        f.close()
     
    if calc_type=='vacuum':
        input_data['calculation'] = 'scf'
        energies = []
        vacuums = []
        converged = False
        i = vacuum
        while not converged:
            if vac_dir is not None:
                cell = atoms.get_cell().array
                cell[vac_dir-1][vac_dir-1] = i
                atoms.set_cell(cell)
            input_data['outdir'] = f'{pwd}/vacuum/{i}'
            calc.set(input_data = input_data)
            atoms.calc = calc
            os.system(f'mkdir -p {pwd}/vacuum/{i}')
            os.chdir(f'{pwd}/vacuum/{i}')
            print('########', i)
            e = atoms.get_potential_energy()
            energies.append(e)
            vacuums.append(i)
            if len(energies) > 2 and abs(energies[-1]-energies[-2]) < threshold and abs(energies[-3]-energies[-2]) < threshold:
                converged = True
            else:
                i = i+1
        os.chdir(pwd)
        f = open('vacuum_conv', 'a')
        for i in range(len(vacuums)):
            st = f'{vacuums[i]}   {energies[i]}\n'
            f.write(st)
        f.close()

    if calc_type=='vc-relax':
        input_data['calculation'] = 'vc-relax'
        
        if vac_dir==None:
            pass
        elif vac_dir==1:
            input_data['cell_dofree'] = '2Dyz'
        elif vac_dir==2:
            input_data['cell_dofree'] = '2Dxz'
        elif vac_dir==3:
            input_data['cell_dofree'] = '2Dxy'

        input_data['outdir'] = f'{pwd}/vc-relax/'
        input_data['forc_conv_thr'] = 1e-6
        calc.set(input_data = input_data)
        atoms.calc = calc
        os.system(f'mkdir -p {pwd}/vc-relax/')
        os.chdir(f'{pwd}/vc-relax/')
        atoms.get_potential_energy()
        os.chdir(pwd)

    if calc_type=='scf':
        input_data['calculation'] = 'scf'
        input_data['outdir'] = f'{pwd}/scf'
        calc.set(input_data=input_data, kpts=kpts)
        atoms.calc = calc
        print(os.getcwd()[-5:])
        os.system(f'mkdir -p {pwd}/scf/')
        os.chdir(f'{pwd}/scf/')
        atoms.get_potential_energy()
        os.chdir(pwd)

    if calc_type=='nscf':
        input_data['calculation'] = 'nscf'
        input_data['outdir'] = './scf'
        input_data['verbosity'] = 'high'
        calc.set(input_data=input_data, kpts=kpts)
        atoms.calc = calc
        print(os.getcwd()[-5:])
        atoms.get_potential_energy()
        os.chdir(pwd)

    if calc_type=='bands':
        input_data['calculation'] = 'bands'
        input_data['outdir'] = './scf'
        input_data['verbosity'] = 'high'
        bl = atoms.get_cell().get_bravais_lattice()
        bp = bl.bandpath(npoints=200)
        if band_path is not None:
            kpts = {'path': band_path, 'npoints':200}
        else:
            kpts = {'path': bp.path, 'npoints':200}
        calc.set(input_data=input_data, kpts=kpts)
        atoms.calc = calc
        print(os.getcwd()[-5:])
        calc.calculate(atoms, ['charges'])
        
        import xml.etree.ElementTree as ET
        from ase.units import Ha, eV
        import numpy as np
        
        tree = ET.parse(f'./scf/{atoms.get_chemical_formula()}.xml')
        root = tree.getroot()
        
        fe = 0
        for i in root.iter('fermi_energy'):
            fe = float(i.text)*Ha/eV

        print(fe)
       
        #emaxx = 0; eminn =0
        aa = []
        for i in root.iter('eigenvalues'):
            aa.append(i.text.split())

        bb = np.array([[float(j) for j in i] for i in aa])
        if emax is None:
            emax = np.max(bb)*Ha/eV
        if emin is None:
            emin = np.min(bb)*Ha/eV

        filename = bp.path
        if band_path is not None:
            filename = band_path

        bs = atoms.calc.band_structure()    
        aa = bs.plot(emin=emin, emax=emax)
        aa.hlines(fe, 0, 10, linestyle='dashed')
        ff = aa.get_figure()
        ff.savefig(f'{atoms.get_chemical_formula()}_{filename}.svg')
        os.chdir(pwd)

    if calc_type=='pressure':

        input_data['calculation'] = 'scf'
        calc.set(input_data=input_data, kpts=kpts)
        ip = get_pressure(structure)

        compressions = [1]
        pressures = [ip]
           
        right = 1.0
        left = float(ic)

        cell = atoms.get_cell().array
        cell *= left
        atoms.set_cell(cell, scale_atoms=True)
        input_data['outdir'] = f'{pwd}/pressure/{left}'
        calc.set(input_data = input_data)
        atoms.calc = calc
        os.system(f'mkdir -p {pwd}/pressure/{left}')
        os.chdir(f'{pwd}/pressure/{left}')
        print('########', left)
        e = atoms.get_potential_energy()
        ip = get_pressure('espresso.pwo')
        compressions.append(left)
        pressures.append(right)

        if ip<rp:
            print(f'Initial compression {left} gave pressure of {ip}, try to decrease compression')
        
        else:

            while True:
                
                if abs(ip - rp) < threshold:
                    write(f'{pwd}/pressure.in', atoms, format='espresso-in')
                    break
                
                else:    
                    atoms = read(f'{pwd}/{structure}')
                    c = (left+right)*0.5
                    cell = atoms.get_cell().array
                    cell *= c
                    atoms.set_cell(cell, scale_atoms=True)
                    input_data['outdir'] = f'{pwd}/pressure/{c}'
                    calc.set(input_data = input_data)
                    atoms.calc = calc
                    os.system(f'mkdir -p {pwd}/pressure/{c}')
                    os.chdir(f'{pwd}/pressure/{c}')
                    print('########', c)
                    e = atoms.get_potential_energy()
                    ip = get_pressure('espresso.pwo')
                    compressions.append(c)
                    pressures.append(ip)

                    if ip > rp:
                        left = c
                    elif ip < rp:
                        right = c
        os.chdir(pwd)
        f = open('pressures', 'a')
        for i in range(len(pressures)):
            f.write(f'{compressions[i]}   {pressures[i]}\n')
        f.close()

    if calc_type == 'eos':
        from ase.eos import EquationOfState as EoS
        import numpy as np
        from ase.units import kJ
        e = []; v = []
        os.mkdir('./eos')
        for i in np.linspace(0.95, 1.1, ns):
            os.mkdir(f"./eos/{round(i,4)}")
            os.chdir(f"./eos/{round(i,4)}")
            cell = atoms.get_cell().array
            atoms.set_cell(cell*i, scale_atoms=True)
            atoms.calc = calc
            e.append(atoms.get_potential_energy())
            v.append(atoms.get_volume())
            os.chdir(pwd)

        bm = EoS(v, e)
        v0, e0, B = bm.fit()
        bm.plot('./eos.png')
        f = open('./eos.dat', 'a')
        f.write(f'''V0 = {v0} Ang,
        E0 = {e0} eV,
        B = {B/kJ*1.0e24} GPa''')
        f.close()

    if calc_type == 'harmonic':
        
        try:
          import spglib as sg
        except:
          pass

        positions = atoms.get_positions()
        

        cell = (atoms.get_cell(), atoms.get_scaled_positions(), atoms.get_atomic_numbers())

        if aid is None:
          aids = np.unique(sg.get_symmetry(cell, symprec=1e-5)['equivalent_atoms'])
        else:
          aids = [ aid ] 
        
        print(aids)

        if dd is None:
          dds = [0,1,2]
        else:
          dds = [dd]
        for Aid in aids:
          for Dd in dds:
            folder = f'{Aid}_{Dd}_harmonic'
            os.system(f'mkdir -p {folder}')
            disps = []
            ens = []
            forces = []
            for i in np.linspace(-0.1, 0.1, 11):
              try:
                prev = read(f'{pwd}/{folder}/{round(i,4)}/espresso.pwo')
                en = prev.get_potential_energy()
                f = prev.get_forces()[Aid][Dd]
              except:
                os.system(f'mkdir -p {pwd}/{folder}/{round(i,4)}')
                os.chdir(f'{pwd}/{folder}/{round(i,4)}')
                pos = positions.copy()
                pos[Aid][Dd] += i
                atoms.set_positions(pos)
                atoms.calc = calc
                en = atoms.get_potential_energy()
                f = atoms.get_forces()[Aid][Dd]
              disps.append(i)
              ens.append(en)
              forces.append(f)
              os.chdir(f'{pwd}/{folder}')

            os.chdir(pwd)


            zzz = np.polyfit(disps, ens, 3)
            ppp = np.poly1d(zzz)
            xxx = np.linspace(-0.12, 0.12, 100)
            fit = ppp(xxx)

            fit2 = np.polyfit(disps, ens, 2)
            pn2 = np.poly1d(fit2)
            errors = np.array(ens)-pn2(disps)

            fig, ax = plt.subplots()

            ax.scatter(disps, ens)
            ax.plot(xxx, fit)
            ax.set_title(f"E0 = {round(zzz[-1],4)}; E1 = {round(zzz[-2],4)}; E2 = {round(zzz[-3],4)}; E3 = {round(zzz[-4],4)}")
            ax.set_xlabel('Displacement')
            ax.set_ylabel('Energy')

            ax2 = ax.twinx()
            ax2.plot(disps, forces, 'g-')
            ax2.set_ylabel('Force')
            fig.savefig(f'{folder}.png')
            
            f = open(f'{pwd}/{folder}.dat', 'w')
            f.write('Disp    Energy    Force    Error_from_fit2\n')
           
            for i in range(len(disps)):
                f.write(f"{round(disps[i],4)}   {round(ens[i],4)}   {round(forces[i],4)}   {round(errors[i],7)}\n")
            f.write(f"E0 = {round(zzz[3],4)}; E1 = {round(zzz[2],4)}; E2 = {round(zzz[1],4)}; E3 = {round(zzz[0],4)}\n")
            f.close()

    def write_ph_input(case='pre', qpt=0):
        if case == 'pre':
            ph_data['start_q'] = 1
            ph_data['last_q'] = 1
            ph_data['recover'] = '.false.'
            ph_data['start_irr'] = 0
            ph_data['last_irr'] = 0

        if case == 'mid':
            ph_data['start_q'] = qpt
            ph_data['last_q'] = qpt
            ph_data['recover'] = '.false.'

        if case == 'post':
            ph_data.pop('start_q')
            ph_data.pop('last_q')
            ph_data['recover'] = '.true.'

        line = dict_to_string(ph_data)
        f = open(f'ph_{case}_{qpt}.in', 'w')
        f.write(f'''
    &INPUTPH
    {line}
    /        
        ''')
        f.close()

    def get_nqpts():
        g = open('ph_pre_0.out', 'r')
        nqpts = int(g.readlines()[-1].split()[0])
        g.close()
        return nqpts

    if calc_type == 'ph_pre':
        os.system('mkdir -p phonons')
        os.chdir('phonons')
        write_ph_input()
        os.system(f'{parallel} -n {ppn} ph.x -in ph_pre_0.in | tee ph_pre_0.out')
        os.chdir(pwd)

    if calc_type == 'ph_mid':
        os.system('mkdir -p phonons')
        os.chdir('phonons')
        
        if nq is None:
            nq = get_nqpts()
        
        for i in range(1, nq+1):
            write_ph_input(case='mid', qpt=i)
        f = open('ph_script.sh', 'w')
        print(nq)
        string = f'''#! /bin/bash
        for ((j=1;j<={nq};j+=1))
        do
        if ! [ -f start_ph_$j ]
        then
        touch start_ph_$j
        {parallel} -n {ppn} ph.x -in ph_mid_$j.in | tee ph_mid_$j.out
        fi
        done'''
        f.write(string)
        f.close()

        os.system('bash ph_script.sh')
        os.chdir(pwd)

    if calc_type == 'ph_post':
        os.system('mkdir -p phonons')
        os.chdir('phonons')
        write_ph_input(case='post')
        os.system(f'{parallel} -n {ppn} ph.x -in ph_post_0.in | tee ph_post_0.out')

        f = open('q2r.in', 'w')
        f.write(f'''
        &INPUT
        zasr='{asr}'
        flfrc='harmonic_flfrc.dat'
        fildyn='{prefix}.dyn_q'
        /
        ''')
        f.close()
        os.system(f'{parallel} -n {ppn} q2r.x -in q2r.in | tee q2r.out')
        os.chdir(pwd)

    if calc_type == 'ph_bands':
        os.system('mkdir -p phonons')
        os.chdir('phonons')
        if band_path is not None:
            spoints = bandpath(band_path, atoms.get_cell(), 100).kpts
        else:
            bp = atoms.cell.bandpath()
            band_path = bp.path.split(',')[0]
            sps = bp.special_points
            spoints = [sps[i] for i in band_path]
        npoints = len(spoints)
        natoms = atoms.get_global_number_of_atoms()

        path = ''
        for i in spoints:
            path += f'{i[0]} {i[1]} {i[2]} 200 \n'

        f = open('matdyn.in', 'w')
        f.write(f'''&input
        asr = '{asr}'
        flfrc = 'harmonic_flfrc.dat'
        flfrq = 'matdyn.freq'
        q_in_band_form = .true.
        q_in_cryst_coord = .true.
        /
        {npoints}
        {path}
        ''')
        f.close()

        string = f'{parallel} -n {ppn} matdyn.x -in matdyn.in > matdyn.out'
        os.system(string)

        a = np.loadtxt("matdyn.freq.gp")
        for i in range(len(a[0])-1):
            plt.plot(a[:,0], a[:,i+1], 'k-')
        plt.xlim(a[0][0], a[-1][0])
        plt.ylim(0, np.max(a[:,-1]))
        plt.vlines([a[:,0][i*200] for i in range(npoints)], 0, np.max(a[:,-1]), linestyles='dashed')
        plt.xticks([a[:,0][i*200] for i in range(npoints)], [i for i in band_path])
        plt.savefig('ph_bands.svg', dpi=600)
        
        os.chdir(pwd)

    if calc_type == 'ph_dos':
        os.system('mkdir -p phonons')
        os.chdir('phonons')
        f = open('ph_dos.in', 'w')
        f.write(f'''
        &input
        asr = '{asr}'
        flfrc = 'harmonic_flfrc.dat'
        flfrq = 'ph_dos.freq'
        dos = .true.
        fldos = 'ph_dos.dat'
        deltaE = 1e-2
        nk1 = {kgrid[0]}, nk2 = {kgrid[1]}, nk3 = {kgrid[2]},
        /
        ''')
        f.close()

        string = f'{parallel} -n {ppn} matdyn.x -in ph_dos.in > ph_dos.out'
        os.system(string)

        a = np.loadtxt("ph_dos.dat")
        plt.plot(a[:,0], a[:,1], 'k-', label='TDOS')
        for i in range(len(a[0])-2):
            plt.plot(a[:,0], a[:,i+2], '--', label=i) 
        plt.xlim(a[:,0][0], a[:,0][-1])
        plt.ylim(0, np.max(a[:,1])+1e-3)
        plt.legend()
        plt.savefig('ph_dos.svg', dpi=600)

        os.chdir(pwd)

    if calc_type == 'epw_pre':
        os.system('mkdir -p epw')
        os.chdir('epw')
        calc = Espresso(pseudopotentials = pseudos)
        cmnd = f"printf '1\n\n{kgrid[0]}\n{kgrid[1]}\n{kgrid[2]}\n0\n0\n0\nyes\n' | kpoints.x"
        os.system(cmnd)
        kpts = get_kpts('mesh_k')
        input_data['calculation'] = 'nscf'
        input_data['outdir'] = f'{pwd}/scf'
        input_data['verbosity'] = 'high'
        calc.set(input_data=input_data)
        calc.write_input(atoms=atoms)
        os.system("sed '/K_POINTS/d' espresso.pwi > tmp.in")
        
        nkpts = len(kpts)
        kpt_lines = f'K_POINTS crystal\n{nkpts}\n'
        for i in kpts:
            kpt_lines+=f'{i[0]}  {i[1]}  {i[2]} 1\n'
        f = open('kptfile', 'w')
        f.write(kpt_lines)
        f.close()

        os.system("cat tmp.in kptfile > nscf.in")
        os.system("rm tmp.in mesh_k espresso.pwi kptfile")
        os.system(f'{parallel} -n {ppn} pw.x -npool {ppn} -in nscf.in | tee nscf.out')
        os.chdir(pwd)
        
        try:
            os.system("mkdir -p epw/save")
            os.system(f"cp phonons/{prefix}.dyn* epw/save")
            os.system("cp -r scf/_ph0/*phsave epw/save")
            os.system("cp scf/_ph0/*dvscf* epw/save")
            phqid = 2
            not_done = True
            while not_done:
                if os.path.isdir(f"scf/_ph0/{prefix}.q_{phqid}/"):
                    os.system(f"cp scf/_ph0/{prefix}.q_{phqid}/*dvscf* epw/save/{prefix}.dvscf_q{phqid}")
                    phqid += 1
                else:
                    not_done = False
        except:
            print('Phonon calculations are incomplete!\nUnable to copy phonon related files\n')


    if calc_type == 'epw_post':
        os.chdir('epw')
        epw_data['nk1'] = kgrid[0]
        epw_data['nk2'] = kgrid[1]
        epw_data['nk3'] = kgrid[2]

        f = open('epw.in', 'w')
        line = dict_to_string(epw_data)
        f.write(f'''
        &inputepw
        {line}
        wdata(1) = 'kmesh_tol = 1e-5'
        /
        ''')
        f.close()

        os.system(f'{parallel} -n {ppn} epw.x -npool {ppn} -in epw.in | tee epw.out')

    if calc_type == 'dos':
        line = dict_to_string(dos_data)
        f = open('dos.in', 'w')
        f.write(f'&DOS\n{line}/\n')
        f.close()
        os.system(f'{parallel} -n {ppn} dos.x -in dos.in | tee dos.out')
        with open(f'{prefix}.dos', 'r') as f:
            l = f.readline()
            fermi = float(l.split()[-2])
        data = load_data(f'{prefix}.dos', head=1)
        plt.plot(data[:,0], data[:,1])
        plt.vlines(fermi,np.min(data[:,1]),np.max(data[:,1]),
                   colors='black', linestyles='dashed')
        plt.ylim(0,np.max(data[:,1])+0.2)
        plt.savefig('dos.png',dpi=400)
