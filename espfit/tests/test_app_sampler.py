import pytest
from importlib.resources import files
from espfit.app.sampler import SetupSampler


# GLOBAL VARIABLES
ESPALOMA_FORCEFIELD = str(files('espfit').joinpath('data/forcefield/espaloma-0.3.2.pt'))


@pytest.fixture
def test_create_test_espaloma_system(tmpdir):
    """Fixture function to create a test system.

    Returns
    -------
    c : espfit.app.sampler.SetupSampler
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/nucleoside/target.pdb')   # PosixPath
    c = SetupSampler(small_molecule_forcefield=ESPALOMA_FORCEFIELD, output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file)  # Exports solvated system as pdb file automatically.

    return c


def test_create_nucleoside_espaloma_system(tmpdir):
    """Test creating nucleoside system using espaloma forcefield.
    
    All solute atoms will be parameterized using the espaloma forcefield.

    Returns
    -------
    None
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/nucleoside/target.pdb')
    c = SetupSampler(small_molecule_forcefield=ESPALOMA_FORCEFIELD, output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file)


def test_create_protein_ligand_espaloma_system(tmpdir):
    """Test creating protein-ligand system using espaloma forcefield.
    
    All solute atoms will be parameterized using the espaloma forcefield.

    Returns
    -------
    None
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/protein-ligand/target.pdb')
    # Convert PosixPath to str to avoid error when loading molecule with RDKIT.
    ligand_file = str(files('espfit').joinpath('data/target/testsystems/protein-ligand/ligands.sdf'))
    c = SetupSampler(small_molecule_forcefield=ESPALOMA_FORCEFIELD, output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file, ligand_file=ligand_file)


def test_create_protein_ligand_openff_system(tmpdir):
    """Test creating protein-ligand system using openff forcefield.
    
    Protein and ligand parameterized with Amber ff14SB and openff-2.1.0, respectively.

    Returns
    -------
    None
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/protein-ligand/target.pdb')
    # Convert PosixPath to str to avoid error when loading molecule with RDKIT.
    ligand_file = str(files('espfit').joinpath('data/target/testsystems/protein-ligand/ligands.sdf'))
    c = SetupSampler(small_molecule_forcefield='openff-2.1.0', output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file, ligand_file=ligand_file)


@pytest.mark.skip("Time demanding test. Skip to speedup the test suite.")
def test_create_protein_espalom_system(tmpdir):
    """Test creating protein system using espaloma force field.
    
    All solute atoms will be parameterized using the espaloma forcefield.

    Returns
    -------
    None
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/protein-ligand/target.pdb')
    c = SetupSampler(small_molecule_forcefield=ESPALOMA_FORCEFIELD, output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file)


@pytest.mark.skip("Time demanding test. Skip to speedup the test suite.")
def test_create_multi_protein_ligand_espaloma_system(tmpdir):
    """Test creating multi-protein and ligand system using espaloma forcefield.
    
    All solute atoms will be parameterized using the espaloma forcefield.
    
    Returns
    -------
    None
    """
    biopolymer_file = files('espfit').joinpath('data/target/testsystems/multi_protein-ligand/target.pdb')
    # Convert PosixPath to str to avoid error when loading molecule with RDKIT.
    ligand_file = str(files('espfit').joinpath('data/target/testsystems/multi_protein-ligand/ligands.sdf'))
    c = SetupSampler(small_molecule_forcefield=ESPALOMA_FORCEFIELD, output_directory_path=str(tmpdir))
    c.create_system(biopolymer_file=biopolymer_file, ligand_file=ligand_file)


def test_export_system(test_create_test_espaloma_system):
    """Test exporting the system to xml files.
    
    Parameters
    ----------
    test_create_test_espaloma_system : espfit.app.sampler.SetupSampler
        Test system instance.

    Returns
    -------
    None
    """
    c = test_create_test_espaloma_system
    c.export_xml()
    

def test_export_system_change_outdir(test_create_test_espaloma_system):
    """Test exporting the system to xml files.
    
    Change the output directory path and check if the new directory is created.

    Parameters
    ----------
    test_create_test_espaloma_system : espfit.app.sampler.SetupSampler
        Test system instance.

    Returns
    -------
    None
    """
    import os
    c = test_create_test_espaloma_system
    old_output_directory_path = c.output_directory_path
    c.export_xml(output_directory_path=os.path.join(old_output_directory_path, 'newdir'))
    
    assert old_output_directory_path != c.output_directory_path


def test_minimize(test_create_test_espaloma_system):
    """Test system minimization.
    
    Parameters
    ----------
    test_create_test_espaloma_system : espfit.app.sampler.SetupSampler
        Test system instance.

    Returns
    -------
    None
    """
    c = test_create_test_espaloma_system
    old_maxIterations = c.maxIterations
    c.maxIterations = 9   # change default
    c.minimize()

    assert old_maxIterations != c.maxIterations


def test_standard_md(test_create_test_espaloma_system):
    """Test standard md simulation.

    Parameters
    ----------
    test_create_test_espaloma_system : espfit.app.sampler.SetupSampler
        Test system instance.

    Returns
    -------
    None
    """
    c = test_create_test_espaloma_system
    c.maxIterations = 10   # update maxIterations to speed up the test
    c.nsteps = 10             
    c.minimize()           # minimize the system before running the simulation to avoid Energy NaN.
    c.run()


def test_create_system_from_xml(test_create_test_espaloma_system):
    """Test creating a system from loading existing xml files.
    
    Parameters
    ----------
    test_create_test_espaloma_system : espfit.app.sampler.SetupSampler
        Test system instance.

    Returns
    -------
    None
    """
    import os
    import glob
    
    c = test_create_test_espaloma_system
    c.export_xml()

    c2 = SetupSampler.from_xml(input_directory_path=c.output_directory_path)
    c2.export_xml(output_directory_path=c.output_directory_path)

    # Check number of exported files. Check state.xml as a representative file.
    # If the same file exists, then suffix number will be added to the file name. 
    n_files = len(glob.glob(os.path.join(c.output_directory_path, 'state*.xml')))
    assert n_files == 2
