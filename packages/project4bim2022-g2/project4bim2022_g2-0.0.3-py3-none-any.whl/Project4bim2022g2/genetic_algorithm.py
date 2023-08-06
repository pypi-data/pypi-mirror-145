# ALl packages import
import numpy as np
import random
import matplotlib.pyplot as plt
from .autoencoder import *


# All function definition

def generation_copies(X, n):
    '''This function generates n copies of the parent X (that will serve to create the final children)
    Args:
        X (np.array) = vector of the latent space of a parent
        n (int) = number of copies we want from this parent
    Return :
        A np.array containing n copies of X '''
    X2 = list(X)
    Y = []
    for i in range(n):
        Y.append(X2)
    return np.array(Y)


def mutation_un_vecteur(parent, step_size, p):
    ''' This function applies a mutation on each element of the latent_vector in each subnp.array of the list Y containing copies of the same parent or recombinations of parents
    Args:
        parent (np.array) : a vector of the latent space
        step_size (float) : parameter of the mutation
        p (float) : probability (between 0 and 1) that there is a mutation for each element of the latent vector
    Return :
        x (np.array) : vecteur modifié muté (avec une probabilité p de mutation pour chaque élément)'''
    n = len(parent)
    for i in range(n):
        if np.random.rand() < p:
            rand = np.random.randn()
            parent[i] += rand*step_size
    return parent


def mutation(Y, step_size, p):
    ''' This function applies a mutation on each vector contained in Y
    Args:
        Y (np.array) : np.array of vectors (latent vectors)
        step_size (float) : parameter of the mutation
        p (float) : probability (between 0 and 1) that there is a mutation for each element of the latent vector
    Return :
        No return : the modification is made directly on Y, and at the end, Y contains len(Y) latent vectors, modified by mutation'''
    n = len(Y)
    for i in range(n):
        Y[i] = mutation_un_vecteur(Y[i], step_size, p)
    return Y


"""def mutation1(Y, step_size, type_evol, p):
    ''' This function applies a mutation on each vector contained in Y
    Args:
        Y (np.array) : np.array of vectors (latent vectors)
        step_size (float) : parameter of the mutation
        type_evol (str) : type of evolution = '+' or ',', depending if we want the parent to be part of the next generation or not
        p (float) : probability (between 0 and 1) that there is a mutation for each element of the latent vector
    Return :
        No return : the modification is made directly on Y, and at the end, Y contains len(Y) latent vectors, modified by mutation (except one if type_evol = '+')'''
    n = len(Y)
    if n == 1:
        if type_evol == ',':
            Y = mutation(Y, step_size, p)
        else :
            X = Y.copy()
            Y = mutation(Y, step_size, p)
            Y.append(X)
    else :
        if type_evol == ',':
            for i in range(n):
                Y[i] = mutation_un_vecteur(Y[i], step_size, p)
        else :
            for i in range(1,n):
                Y[i] = mutation_un_vecteur(Y[i], step_size, p)
    return Y"""


def concatenate_list(X):
    ''''''
    Y = []
    n = len(X)
    if n == 1:
        return X
    else:
        for i in range(1, n):
            for element in X[i]:
                Y = np.vstack([Y, element])
        return Y


def recombination_2parents_moy(X1, X2, p):
    '''Calcule le vecteur obtenu à partir d'une recombinaison à partir des 2 parents X1 et X2, qui calcule la moyenne des coordonnées pour chaque élément des vecteurs latents, avec une probabilité p pour chaque élément
        Sinon, c'est l'un ou l'autre des éléments de X1 ou X2 qui est choisi
    Args :
        X1 (np.array/list): vecteur de l'espace latent, un parent
        X2 (np.array/list) : vecteur de l'espace latent, un parent
        p (float) : probabilité de modifier l'élément à chaque tour de boucle (p entre 0 et 1, si p vaut 1, new_vector est la moyenne de X1 et X2, si p vaut 0, les éléments de new_vector sont extraits soit de X1, soit de X2)
    Return :
        new_vector(np.array) : np.array formant un nouveau vecteur de l'espace latent, avec pour certaines coordonnées celles de X1, pour d'autres celles de X2, pour d'autres la moyenne des 2'''
    n = len(X1)
    new_vector = []
    for i in range(n):
        if np.random.rand() < p:
            x = (X1[i]+X2[i])/2
            new_vector.append(x)
        else:
            if np.random.rand() < 1/2:
                new_vector.append(X1[i])
            else:
                new_vector.append(X2[i])
    return np.array(new_vector)


def recombination_k_parents(X, p):
    '''Calcule le vecteur obtenu à partir d'une recombinaison à partir des k parents de la liste X, qui calcule la moyenne des coordonnées pour chaque élément des vecteurs latents, avec une probabilité p pour chaque élément
        Sinon, on choisit un élément parmi les k vecteurs
    Args :
        X (np.array): Liste de vecteurs de l'espace latent, de longueur k
        p (float) : probabilité de modifier l'élément à chaque tour de boucle (p entre 0 et 1, si p vaut 1, new_vector est la moyenne de X1 et X2, si p vaut 0, les éléments de new_vector sont extraits soit de X1, soit de X2)
    Return :
        new_vector(np.array) : np.array formant un nouveau vecteur de l'espace latent, recombinaison des k parents'''
    k = len(X)
    new_vector = []
    n = len(X[0])
    for i in range(n):
        if np.random.rand() < p:
            x = 0
            for j in range(k):
                x += X[j][i]
            new_vector.append(x/k)
        else:
            rand = np.random.rand()
            proba = 1/k
            for j in range(k):
                if rand <= proba:
                    new_vector.append(X[j][i])
                    break
                proba += 1/k
    return np.array(new_vector)


def fitness_function(X, input_user):
    ''' This function calculates a fitness for each image in the list X according to the choice made by the user : if the image has been chosen by the user, the fitness of this image is set to 1, else, to 0
    Args :
        X (np.array) : list of latent vectors representing the images shown to the user
        input_user (list) : list of numbers corresponding to the images chosen by the user
    Return :
        List_fitness (np.array) : (same dimension as X) list of fitnesses of the images of X, 1 if it has been chosen by the user, 0 otherwise '''
    n = len(X)
    List_fitness = np.zeros(n)
    for i in range(n):
        if i in input_user:
            List_fitness[i] = 1
    return List_fitness


def selection_function(X, fitness_function):
    '''input_user doit être défini globalement'''
    List_fitness = fitness_function(X, input_user)
    n = len(X)
    X_selected = []
    for i in range(n):
        if List_fitness[i] == 1:
            X_selected.append(X[i])
    return X_selected


def selection_function2(X, input_user):
    ''''''
    n = len(X)
    X_selected = []
    for num in input_user:
        X_selected.append(X[num])
    return X_selected


def user_choice(List_images, n):  # à modifier pour être ok avec l'interface graphique
    '''This function asks the user to choose between len(List_images) images the n images that are the closest to the suspect
    Args:
        List_images (list): List of images displayed on the screen, generated by the algorithm or randomly chosen in the database
        n (int): number of images  to be chosen by the user, has to be < len(List_images)
    Returns:
        list : list of images (an image = a list of pixels) chosen by the user'''
    List_num = []
    List_images_chosen = []
    str_images_chosen = input(
        f"Choose {n} images among those displayed that are the closest to the suspect and write the position of each image chosen separated by a coma (ex : 1,5 = 1st image, 5th one) :  ")
    List_num_str = str_images_chosen.split(',')
    for element in List_num_str:
        List_num.append(int(element))
    for number in List_num:
        i = number - 1
        List_images_chosen.append(List_images[i])
    return List_images_chosen


def one_iteration_mutation(List_parents, type_evol, n, step_size):
    '''This function calculates the next generation of children from a list of parents. The children are generated only by mutation here, according to the type of evolution str_images_chosen
    Args :
        List_parents (np.array/list) : list of parents that we want to generate children the next generation
        type_evol (str) : type of evolution, '+' if we want the parent to be part of the next generation, ',' otherwise
        n (int) : number of children we want to be generated from each parents
        step_size (float) : parameter of mutation
    Return :
        List (np.array) of latent vectors that are the children of the parents in List_parents, length should be n*len(List_parents) if type_evol == ',', and (n+1)*len(List_parents) otherwise'''
    L_children = []
    for parent in List_parents:
        # print(parent)
        if type_evol == '+':
            Parent = generation_copies(parent, n)
            # print(Parent)
            Children = mutation(Parent, step_size, 1)
            #print("Enfants générés par mutation",Children)
            Children = np.vstack([Children, parent])
            #print("Enfants après ajout parent", Children)
            # print(Children)
            for element in Children:
                # print(element)
                L_children.append(element)
            #print("Longueur liste Enfants", len(L_children))
        else:
            Parent = generation_copies(parent, n)
            Children = mutation(Parent, step_size, 1)
            # print(Children)
            for element in Children:
                L_children.append(element)
        #print("Liste de tous les enfants concaténés", concatenate_list(L_children))
    return np.array(L_children)


def adjust_children(List_parents, prior):
    ''''''
    n = len(List_parents)
    if n == 1:
        L = one_iteration_mutation(List_parents, ',', 4, 1.5)
        L = np.vstack([L, one_iteration_mutation(List_parents, '+', 3, 1)])
        # print(L)
        new_images = generate_latent_vectors(prior, 2)
        L = np.vstack([L, new_images])
        # print(L)
        # random.shuffle(L)
        return L
    elif n == 2:
        L = one_iteration_mutation(List_parents, ',', 3, 1.5)
        new_images = generate_latent_vectors(prior, 2)
        L = np.vstack([L, new_images])
        recombination1 = recombination_k_parents(List_parents, 1)
        recombination2 = recombination_k_parents(List_parents, 0)
        L = np.vstack([L, recombination1])
        L = np.vstack([L, recombination2])
        return L
    elif n == 3:
        L = one_iteration_mutation(List_parents, ',', 2, 1.5)
        new_images = generate_latent_vectors(prior, 2)
        L = np.vstack([L, new_images])
        recombination1 = recombination_k_parents(List_parents, 1)
        recombination2 = recombination_k_parents(List_parents, 0)
        L = np.vstack([L, recombination1])
        L = np.vstack([L, recombination2])
        return L
    elif n == 4:
        L = one_iteration_mutation(List_parents, ',', 1, 1.5)
        new_images = generate_latent_vectors(prior, 2)
        L = np.vstack([L, new_images])
        recombination1 = recombination_k_parents(List_parents, 1)
        recombination2 = recombination_k_parents(List_parents, 0)
        recombination3 = recombination_k_parents(
            [List_parents[0], List_parents[1]], 0)
        recombination4 = recombination_k_parents(
            [List_parents[2], List_parents[3]], 1)
        L = np.vstack([L, recombination1])
        L = np.vstack([L, recombination2])
        L = np.vstack([L, recombination3])
        L = np.vstack([L, recombination4])
        return L
    # elif n == 5 :


def one_iteration_recombination(List_parents, type_evol, n, step_size):
    ''''''
    pass


def calcul_distance(parent, L_enfants):
    ''''''
    pass


def strategy_1_lambda(List_init_img, type_evol, nbre_iter):
    ''''''
    # rajouter fonction qui fait apparaitre l'image
    img = user_choice(List_init_img, 1)
    for _ in range(nbre_iter):
        List_children = generation_enfants(12, img, type_evol)

        img = selection_function2(List_children)

    pass


def strategy_mu_lambda(X, type_evol, nbre_iter):
    pass


def strategy_mu_ro_lambda(X, type_evol, nbre_iter):
    pass


def genetic_algorithm(List_latent_vectors):
    # d'abord étape de sélection
    mu = 4
    lambda_ = 12
    n = len(List_latent_vectors)
    if n == 1:
        strategy_1_lambda


# Main program
if __name__ == "__main__":
    X = np.array([[1.0, 2.0, 3.0], [2.0, 5.0, 9.0]])
    # print(X)
    #Y = mutation(X,1, 1)
    # print(Y)
    X1 = np.array([1.0, 2.0, 3.0])
    X2 = np.array([5.0, 6.0, 7.0])
    X3 = recombination_2parents_moy(X1, X2, 1)
    # print(X3)
    X4 = recombination_k_parents(X, 0)
    # print(X4)
    Y = one_iteration_mutation([X1], '+', 3, 1)
    print(Y)
